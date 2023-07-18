/* 
 * https://www.cs.cmu.edu/afs/cs/academic/class/15213-f99/www/class26/udpclient.c
 * udpclient.c - A simple UDP client
 * usage: udpclient <host> <port>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define BUFSIZE 3 * 512

unsigned char static_buffer[3*512];

/**
 * die - wrapper for perror
 */
void die(const char *msg) {
  perror(msg);
  exit(EXIT_FAILURE);
}

int main(int argc, char **argv) {

  /* check command line arguments */
  if (argc != 4) {
    fprintf(stderr, "Usage: %s <hostname> <port> <count>\n", argv[0]);
    exit(0);
  }
  char* hostname = argv[1];
  int portno = atoi(argv[2]);
  int packet_count = atoi(argv[3]);

  /* socket: create the socket */
  int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0) {
    die("ERROR opening socket");
  }

  /* gethostbyname: get the server's DNS entry */
  /* TODO: use getaddrinfo */
  struct hostent *server = gethostbyname(hostname);
  if (server == NULL) {
    fprintf(stderr, "ERROR, no such host as %s\n", hostname);
    exit(0);
  }

  /* build the server's Internet address */
  struct sockaddr_in serveraddr;
  memset(&serveraddr, 0, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  memcpy(&serveraddr.sin_addr.s_addr, (char *)server->h_addr, server->h_length);
  serveraddr.sin_port = htons(portno);

  /* send the message to the server */
  while (packet_count--) {
    int n = sendto(sockfd, static_buffer, BUFSIZE, 0,
                   (const struct sockaddr*)&serveraddr, sizeof(serveraddr));
    if (n < 0) {
      die("ERROR in sendto");
    }
  }
  
  return 0;
}
