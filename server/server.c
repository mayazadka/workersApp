#include "server.h"

int stop = 0;

int main(void) {
    char line[MAX_MESSAGE_SIZE] = "";
    int sock;
    int error;

    if((error = openServer(PORT, &sock))!=SUCCESS){exit(error);}

    puts("enter something to close the server:");
    scanf("%s", line);

    closeServer(sock);

    return SUCCESS;
}


// opening a new server and running it in a seperted thread (using runServer method)
int openServer(int port, int* sock)
{
	pthread_t tid;
	struct sockaddr_in server_name;
	Main_data* main_data;
	
	*sock = socket(AF_INET,SOCK_STREAM,0);
	if(*sock < 0){return ERROR;}

	bzero(&server_name,sizeof(server_name));
	server_name.sin_family = AF_INET;
	server_name.sin_addr.s_addr = htonl(INADDR_ANY);
	server_name.sin_port = htons(port);
	
	if(bind(*sock, (struct sockaddr *)&server_name, sizeof(server_name)) < 0)
	{
		close(*sock);
		return ERROR;
	}
	
	if(listen(*sock,MAX_CLIENTS) < 0)
	{
		close(*sock);
		return ERROR;
	}

	main_data = (Main_data*)malloc(sizeof(Main_data));
	if(main_data == NULL)
	{
		close(*sock);
		return ERROR;
	}
	main_data->sock = *sock;
	main_data->server_name = server_name;	

	pthread_create(&tid, NULL, runServer, main_data);
	
	return SUCCESS;
}

// listening until the server is told to stop, any time we accept a new client we handle him in a new thread (via clientHandel method)
void* runServer(void* args)
{
	pthread_t tid;
	Main_data* main_data = args;
	socklen_t len = sizeof(main_data->server_name);
	int place;
	char buf[1000];
	Strings argumants;
	int client_sock;
	
	stop = 0;
	while(!stop)
	{
		if(main_data->sock == NULL)
		{
			close(main_data->sock);
			// return error?
		}
		
		client_sock = accept(main_data->sock, (struct sockaddr *)&main_data->server_name,&len);
		if(client_sock<0) {break;}
		
		int n = read(client_sock, buf, 1000); //read first command from client
		buf[n] = '\0';
		argumants = split(buf);
		// hashed_password plain_text salt 
		if(strcmp(argumants.strings[0], "hashed_password")==0){
			char * hashed = GenerateSaltedHash(argumants.strings[1],argumants.strings[2]);
			write(client_sock, hashed, strlen(hashed));
		}
		// create_salt
		else if(strcmp(argumants.strings[0], "create_salt")==0){
			char* salt = getSalt();
			write(client_sock, salt, strlen(salt));
		}
		else{continue;}
		
		close(client_sock);
	}

	write(client_sock, "bye", 3);
	close(client_sock);


	free(main_data);
	return NULL;
}

// closing the server
void closeServer(int sock)
{
	stop = 1;
	shutdown(sock, SHUT_RDWR);
	close(sock);
}
