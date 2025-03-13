#include <thread>
#include <iostream>
#include <random>
#include <vector>
#include <atomic>

using namespace std;

const int NUM_PHILOSOPHERS = 5; // Number of philosophers

struct Fork
{
	bool isFree = true;
};

std::vector<Fork> forks;

int generateRandomInt()
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distrib(1, 10);
	int random_number = distrib(gen);
	return random_number;
}

void philosopher(int id, std::atomic<bool>& stop)
{
	int left_fork_id = id;
	int right_fork_id = (id + 1) % NUM_PHILOSOPHERS; // To enable circle
	bool hasLeftFork = false;
	bool hasRightFork = false;

	while (!stop)
	{
		cout << "Philosopher " << id << " is thinking." << endl;
		this_thread::sleep_for(chrono::seconds(generateRandomInt()));
		cout << "Philosopher " << id << " try to eat." << endl;
		while (!(hasLeftFork && hasRightFork))
		{
			if (forks[left_fork_id].isFree)
			{
				cout << "Philosopher " << id << " grab left fork" << left_fork_id << "." << endl;
				this_thread::sleep_for(chrono::seconds(generateRandomInt()));
				hasLeftFork = true;
				forks[left_fork_id].isFree = false;
				continue;
			}
			if (forks[right_fork_id].isFree)
			{
				cout << "Philosopher " << id << " grab right fork" << right_fork_id << "." << endl;
				this_thread::sleep_for(chrono::seconds(generateRandomInt()));
				hasRightFork = true;
				forks[right_fork_id].isFree = false;
				continue;
			}
			std::this_thread::sleep_for(std::chrono::seconds(1));
		}
		cout << "Philosopher " << id << " is eating." << endl;
		std::this_thread::sleep_for(std::chrono::seconds(generateRandomInt()));
		hasLeftFork = false;
		hasRightFork = false;
		cout << "Philosopher " << id << " finished eating." << endl;
		forks[left_fork_id].isFree = true;
		forks[right_fork_id].isFree = true;
	}
}

int main()
{
	//cout << "Enter the number of philosophers: ";
	//cin >> NUM_PHILOSOPHERS;

	std::atomic<bool> stop(false);

	for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
		forks.push_back(Fork());
	}

	std::vector<std::thread> philosophers;
	for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
		philosophers.emplace_back(philosopher, i, std::ref(stop));
	}

	// Let the philosophers run for a while
	std::this_thread::sleep_for(std::chrono::seconds(30));

	// Stop the philosophers
	stop = true;

	// Wait for all philosophers to finish
	for (auto& ph : philosophers) {
		ph.join();
	}

	return 0;
}