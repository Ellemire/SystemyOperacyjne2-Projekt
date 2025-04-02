#include <thread>
#include <iostream>
#include <random>
#include <vector>
#include <atomic>
#include <mutex>
#include <memory>	// For access to structure
#include <cstdlib>	// For casting to int

using namespace std;

const int TIME = 360;	// Duration of simulation in seconds
int NUM_PHILOSOPHERS; 	// Number of philosophers
int num_philosophers_eating = 0;	// Numbers of philosophers eating

// Structure that represents fork
struct Fork
{
	bool isFree = true; // Attribute to show if fork is free (true) or taken (false)
	mutex fork_mutex;	// Mutex to synchronize access to fork
};

vector<unique_ptr<Fork>> forks; // List of forks (using unique_ptr)
mutex console_mutex;            // Mutex to synchronize console output
mutex num_philosophers_eating_mutex;

// Function to generate random integer
int generateRandomInt()
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distrib(1, 10);
	int random_number = distrib(gen);
	return random_number;
}

/* Function that represents philosopher. Philosopher has access to forks with his id (left) and his id incremented (right).
Philosopher repeatedly think, try to eat and eat. 
When philosopher try to eat he start with trying to grab left fork then right fork in loop till he get both forks. */  
void philosopher(int id, atomic<bool>& stop)
{
    int left_fork_id = id;
    int right_fork_id = (id + 1) % NUM_PHILOSOPHERS; // To enable circle
    bool hasLeftFork = false;
    bool hasRightFork = false;
	bool try_to_eat = false;

    while (!stop)
    {
        {
            lock_guard<mutex> lock(console_mutex);
            cout << "Philosopher " << id << " is thinking." << endl;
        }
        this_thread::sleep_for(chrono::seconds(generateRandomInt()));

        {
            lock_guard<mutex> lock(console_mutex);
            cout << "Philosopher " << id << " try to eat." << endl;
        }
		try_to_eat = true;

		while (try_to_eat)
		{
			{
				lock_guard<mutex> lock(num_philosophers_eating_mutex);
				if (num_philosophers_eating < NUM_PHILOSOPHERS - 1)
				{
					try_to_eat = false;
					num_philosophers_eating++;
					{
						lock_guard<mutex> lock(console_mutex);
						cout << "Philosopher " << id << " can eat." << endl;
						cout << "Philosophers eating: " << num_philosophers_eating << endl;
					}
					break;
				}
			}
			{
				lock_guard<mutex> lock(console_mutex);
				cout << "Philosophers eating: " << num_philosophers_eating << endl;
				cout << "Philosopher " << id << " is denied to eat." << endl;
			}
			this_thread::sleep_for(chrono::seconds(2));
		}

        while (!(hasLeftFork && hasRightFork))
        {
            if (forks[left_fork_id]->isFree)
            {
                lock_guard<mutex> lock(forks[left_fork_id]->fork_mutex);
                if (forks[left_fork_id]->isFree) // Double-check after locking
                {
                    {
                        lock_guard<mutex> lock(console_mutex);
                        cout << "Philosopher " << id << " grab left fork " << left_fork_id << "." << endl;
                    }
                    this_thread::sleep_for(chrono::seconds(generateRandomInt()));
                    hasLeftFork = true;
                    forks[left_fork_id]->isFree = false;
                }
            }
            if (forks[right_fork_id]->isFree)
            {
                lock_guard<mutex> lock(forks[right_fork_id]->fork_mutex);
                if (forks[right_fork_id]->isFree) // Double-check after locking
                {
                    {
                        lock_guard<mutex> lock(console_mutex);
                        cout << "Philosopher " << id << " grab right fork " << right_fork_id << "." << endl;
                    }
                    this_thread::sleep_for(chrono::seconds(generateRandomInt()));
                    hasRightFork = true;
                    forks[right_fork_id]->isFree = false;
                }
            }
            this_thread::sleep_for(chrono::seconds(1));
        }

        {
            lock_guard<mutex> lock(console_mutex);
            cout << "Philosopher " << id << " is eating." << endl;
        }
        this_thread::sleep_for(chrono::seconds(generateRandomInt()));

        hasLeftFork = false;
        hasRightFork = false;

        {
			lock_guard<mutex> lock(num_philosophers_eating_mutex);
			num_philosophers_eating--;
		}

		{
            lock_guard<mutex> lock(console_mutex);
            cout << "Philosopher " << id << " finished eating." << endl;
        }

        // Release forks
        {
            lock_guard<mutex> lock(forks[left_fork_id]->fork_mutex);
            forks[left_fork_id]->isFree = true;
        }
        {
            lock_guard<mutex> lock(forks[right_fork_id]->fork_mutex);
            forks[right_fork_id]->isFree = true;
        }
    }
}

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        cerr << "Usage: " << argv[0] << " <number_of_philosophers>" << endl;
        return 1;
    }

    NUM_PHILOSOPHERS = atoi(argv[1]);
    if (NUM_PHILOSOPHERS <= 0)
    {
        cerr << "Number of philosophers must be a positive integer." << endl;
        return 1;
    }
	{
		lock_guard<mutex> lock(console_mutex);
		cout << "Number of philosophers set: " << NUM_PHILOSOPHERS << endl;
	}


    atomic<bool> stop(false);

    // Initialize forks using unique_ptr
    for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
        forks.push_back(make_unique<Fork>());
    }

    vector<thread> philosophers;
    for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
        philosophers.emplace_back(philosopher, i, ref(stop));
        {
            lock_guard<mutex> lock(console_mutex);
            cout << "Philosopher " << i << " is initialized." << endl;
        }
    }

    // Stop the philosophers - if you do not want them to run infinitely uncomment lines below
	this_thread::sleep_for(chrono::seconds(TIME));
    stop = true;
    //Wait for all philosophers to finish
    for (auto& ph : philosophers) {
        ph.join();
    }

    return 0;
}