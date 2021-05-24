//includes
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <pthread.h>
#include "password.h"
#include "help.h"

//defines
#define MAX_MESSAGE_SIZE 1024
#define MAX_CLIENTS 1
#define PORT 8888
#define IP "127.0.0.1"
#define SUCCESS 1
#define ERROR 0

//structures
struct main_data{
	pthread_t tid;
	int sock;
	struct sockaddr_in server_name;
}typedef Main_data;

//functions
int openServer(int port, int* sock);
void closeServer(int sock);
void* runServer(void* args);
