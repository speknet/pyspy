/*
Initialise Winsock
*/
#include <stdio.h>;
#include <winsock2.h>
#pragma comment(lib,"ws2_32.lib") //Winsock Library

int newsock()
{
    SOCKET s;
    WSADATA wsa;
    struct sockaddr_in server;
    printf("\nInitialising Winsock...");
    if (WSAStartup(MAKEWORD(2,2),&wsa) != 0)
    {
        printf("Failed. Error Code : %d",WSAGetLastError());
        return 1;
    }
    printf("Initialised.\n");
    //Create a socket
    if((s = socket(AF_INET , SOCK_STREAM , 0 )) == INVALID_SOCKET)
    {
        printf("Could not create socket : %d" , WSAGetLastError());
    }
    printf("Socket created.\n");
    server.sin_addr.s_addr = inet_addr("192.168.56.1");
    server.sin_family = AF_INET;
    server.sin_port = htons( 3320 );
    //Connect to remote server
    if (connect(s , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        puts("connect error");
        return 1;
    }
    puts("Connected");
    return s;
}
int senddata(char *message){
    //Send some data
//    if( send(s , message , strlen(message) , 0) < 0)
//    {
//        puts("Send failed");
//        return 1;
//    }
//    puts("Data Sent\n");
//    return 0;
    //return send(s , &message , sizeof(message) , 0);
}
