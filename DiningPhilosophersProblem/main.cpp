#include <thread>
#include <iostream>
#include <random>
#include <vector>
#include <atomic>
#include <mutex>

using namespace std;

const int NUM_PHILOSOPHERS = 5; // Number of philosophers

// Structure that represents fork
struct Fork
{
	bool isFree = true; // Attribute to show if fork is free (true) or taken (false)
	mutex fork_mutex;	// Mutex to synchronize access to fork
};

vector<Fork> forks;		// List of forks
mutex console_mutex;	// Mutex to synchronize console output


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
		while (!(hasLeftFork && hasRightFork))
		{
			{
				lock_guard<mutex> lock(forks[left_fork_id].fork_mutex);
				if (forks[left_fork_id].isFree)
				{
					
					{
						lock_guard<mutex> lock(console_mutex);
						cout << "Philosopher " << id << " grab left fork " << left_fork_id << "." << endl;
					}
					this_thread::sleep_for(chrono::seconds(generateRandomInt()));
					hasLeftFork = true;
					forks[left_fork_id].isFree = false;
					continue;
				}
			}

			{
				lock_guard<mutex> lock(forks[right_fork_id].fork_mutex);
				if (forks[right_fork_id].isFree)
				{
					{
						lock_guard<mutex> lock(console_mutex);
						cout << "Philosopher " << id << " grab right fork " << right_fork_id << "." << endl;
					}
					this_thread::sleep_for(chrono::seconds(generateRandomInt()));
					hasRightFork = true;
					forks[right_fork_id].isFree = false;
					continue;
				}
			}

			std::this_thread::sleep_for(std::chrono::seconds(1));
		}

		{
			lock_guard<mutex> lock(console_mutex);
			cout << "Philosopher " << id << " is eating." << endl;
		}
		std::this_thread::sleep_for(std::chrono::seconds(generateRandomInt()));

		{
			lock_guard<mutex> lock(console_mutex);
			cout << "Philosopher " << id << " finished eating." << endl;
		}

		// Left fork release
		{
			lock_guard<mutex> lock(forks[left_fork_id].fork_mutex);
			hasLeftFork = false;
			forks[left_fork_id].isFree = true;
			{
				lock_guard<mutex> lock(console_mutex);
				cout << "Philosopher " << id << " relised fork " << left_fork_id << endl;
			}
		}
		// Right fork release
		{
			lock_guard<mutex> lock(forks[right_fork_id].fork_mutex);
			hasRightFork = false;
			forks[right_fork_id].isFree = true;
			{
				lock_guard<mutex> lock(console_mutex);
				cout << "Philosopher " << id << " relised fork " << right_fork_id << endl;
			}
		}
	}
}

int main()
{
	//cout << "Enter the number of philosophers: ";
	//cin >> NUM_PHILOSOPHERS;

	atomic<bool> stop(false);
	forks.reserve(NUM_PHILOSOPHERS);

	for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
		forks.emplace_back(Fork());
	}

	std::vector<std::thread> philosophers;
	for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
		philosophers.emplace_back(philosopher, i, std::ref(stop));
		{
			lock_guard<mutex> lock(console_mutex);
			cout << "Philosopher " << i << " is inicialized." << endl;
		}
	}

	// Let the philosophers run for a while
	std::this_thread::sleep_for(std::chrono::seconds(30));

	// Stop the philosophers
	stop = true;
	{
		lock_guard<mutex> lock(console_mutex);
		cout << "Time is up." << endl;
	}

	// Wait for all philosophers to finish
	for (auto& ph : philosophers) {
		ph.join();
	}

	return 0;
}