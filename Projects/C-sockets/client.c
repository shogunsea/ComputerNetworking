#include <stdio.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <openssl/ssl.h> // libs for ssl connection
//#include <openssl/err.h>
//#include <openssl/rand.h>
//#include <stdlib.h>//  use strtol instead of atoi
#define DEFAULT_SSL_PORT 27994
#define DEFAULT_PORT 27993
#define BUFFER_LENGTH 256//'The maximum length of each message is 256 bytes'
#define MESSAGE_LENGTH 256
#define INITIAL_MESSAGE "cs5700spring2014 HELLO "
#define SOLUTION_LENGTH 100
#define FLAG_LENGTH 64 

int parametersValidation(int parametersCount, char *parameters[]){
    //printf("Validating parameters...\n");
    int result = 0;
    switch(parametersCount){
        case(3):
            result = 1;
            break;
        case(4):
            // Make sure first option is exactly '-s'
            result = strlen(parameters[1])==2&&strncmp(parameters[1],"-s",2)==0;
            break;
        case(5):
            // Make sure first option is exactly '-p' and second option is valid port number.
            result = strlen(parameters[1])==2&&strncmp(parameters[1],"-p",2)==0&&(int)strtol(parameters[2],NULL,10)>0;
            break;
        case(6):
            // printf("case 6\n");
            // Make sure first option is exactly '-p', second option is valid port number, third option is exactly '-s'
            result = strlen(parameters[3])==2&&strlen(parameters[1])==2&&strncmp(parameters[1],"-p",2)==0 && strncmp(parameters[3],"-s",2)==0&&(int)strtol(parameters[2],NULL,10)>0;
            break;
    }
    // if(result==1){
    //     printf("Validation Passed.\n");
    // }else{
    //     printf("Validation Failed.\n");
    // }
    return result;
}


// function to parse mathematical string and evaluate the expression.
int calculator(char *buffer){
    // printf("buffer is: %s\n", buffer );
    char *equation;
    // strncpy ( equation, buffer, sizeof(str2) ); 
    equation =  strstr(buffer, "STATUS ");
    // printf("%i equation is: %s\n", (int)strlen(equation), equation );
    char firstNumber[5]={};
    char secondNumber[5]={};
    int operator=0;
    // cs5700spring2014 STATUS 991 - 574
    // STATUS 991 - 574
    int i=0;
    int j =0;
    for (i=5;i<(int)strlen(equation);i++){
        if(equation[i]=='S'&&equation[i+1]==' '){
            int k=0;
            memset(firstNumber, '\0', 5);
            for(j=i+2;equation[j]!=' ';j++){
                firstNumber[k++]=equation[j];
            }
        }
        // ascii 
        if(equation[i]>41&&equation[i]<48){
            operator = equation[i];
            int k=0;
            memset(secondNumber,'\0',5);
            for(j=i+2;equation[j]!='\n';j++ ){
                secondNumber[k++]=equation[j];
            }
        }
    }
    int first = strtol(firstNumber,NULL,10);
    int second = strtol(secondNumber,NULL,10);
    int result = 0;
    switch(operator){
        case(43):
            result = first + second;
            break;
        case(45):
            result = first - second;
            break;
        case(42):
            result = first * second;
            break;
        case(47):
            result = first / second;
            break;
    }
    return result;
}

void errorHandler(const char *msg){
    printf("%s\n",msg);
    exit(0);
}

void normalConnection(int sfd, char *info){   
    // printf("sfd is:%i\n",sfd);
    // printf("info is:%s\n",info);
    char buffer[BUFFER_LENGTH]={};
    char flagBuffer[BUFFER_LENGTH]={};
    int result=0;
    char solution [SOLUTION_LENGTH] ={};
    
    write(sfd,info,strlen(info));
    read (sfd, buffer,BUFFER_LENGTH);
    
    int a = 0;//count how many questions solved.
    while (strstr(buffer,"BYE")==0){
        a++;
        // printf("calculating!\n");
        // printf("buffer is: %s\n",buffer);
        result = calculator(buffer);
        // printf("result is: %i\n", result);
        // printf("solution before sprintf: %s\n", solution);
        sprintf(solution, "%s %d\n","cs5700spring2014", result);
        // printf("solution after sprintf: %s\n", solution);
        memset(buffer, '\0', BUFFER_LENGTH);
        write(sfd,solution,strlen(solution));
        read (sfd, buffer,BUFFER_LENGTH);
    }
    // printf("Normal Connection:\n");
    // printf("FLAG_LENGTH: %i\n",FLAG_LENGTH);
    // printf("buffer: %s\n", buffer);
    // printf("flagBuffer: %s\n", flagBuffer);
    memcpy(flagBuffer, buffer+sizeof("cs5700spring2014"), FLAG_LENGTH);
    // printf("Your secret flag is: \n%s\n",flagBuffer);
    printf("%s\n",flagBuffer);
    //printf("total %i equations.\n",a);
}
//http://www.openssl.org/docs/ssl/ssl.html   # openssl lib documentation
//http://savetheions.com/2010/01/16/quickly-using-openssl-in-c/   # tutorial for how to use openssl in c
void SSLConnection(int sfd, char *info){
    //printf("Inside ssl function, sockfd: %i\n",sfd);
    SSL *sslHandle;
    SSL_CTX *sslContext;
    // Register the error strings for libcrypto & libssl
    SSL_load_error_strings();
    // Register the available ciphers and digests
    SSL_library_init();
    // New context saying we are a client, and using SSL 2 or 3
    sslContext = SSL_CTX_new (SSLv23_client_method());
    if (sslContext == NULL)
        errorHandler("ERROR SSL context");
    // Create an SSL struct for the connection
    sslHandle = SSL_new (sslContext);
    if (sslHandle == NULL)
        errorHandler("ERROR SSL handle");
    // Connect the SSL struct to our connection
    if(!SSL_set_fd(sslHandle, sfd))
        errorHandler("ERROR SSL set");
     // Initiate SSL handshake
    if(SSL_connect(sslHandle) != 1)
        errorHandler("ERROR SSL connecting");
    char buffer[BUFFER_LENGTH]={};
    char flagBuffer[BUFFER_LENGTH]={};
    int result=0;
    char solution [SOLUTION_LENGTH] ={};
    
    SSL_write (sslHandle, info, strlen (info));
    SSL_read (sslHandle, buffer, BUFFER_LENGTH);
    
    while (strstr(buffer,"BYE")==0){
        result = calculator(buffer);

        sprintf(solution, "%s %d\n","cs5700spring2014",result);
        memset(buffer, '\0', BUFFER_LENGTH);
        SSL_write (sslHandle, solution, strlen (solution));
        SSL_read (sslHandle, buffer, BUFFER_LENGTH);
    }
    memcpy(flagBuffer, buffer+sizeof("cs5700spring2014"), FLAG_LENGTH);

    // printf("Your secret flag is: \n%s\n",flagBuffer);
    printf("%s\n",flagBuffer);

    if(sslHandle) {
        SSL_shutdown(sslHandle);
        SSL_free(sslHandle);
    }
    if(sslContext){
        SSL_CTX_free(sslContext);
    }
}

int main(int parameterCount, char *parameters[]){
    int ssl_flag = 0;
    int socketFileDescriptor;
    int port;
    struct sockaddr_in server_addr;
    struct hostent *h;    
    char info[MESSAGE_LENGTH] =  INITIAL_MESSAGE;
    char theTerminator[] = "\n";
// Naming convetion in c:
// All macros and constants in caps: MAX_BUFFER_SIZE, TRACKING_ID_"cs5700spring2014".
// Struct names and typedef's in camelcase: GtkWidget, TrackingOrder.
// Functions that operate on structs: classic C style: gtk_widget_show(), tracking_order_process().
// Pointers: nothing fancy here: GtkWidget *foo, TrackingOrder *bar.
// Global variables: just don't use global variables. They are evil.
// Functions that are there, but shouldn't be called directly, or have obscure uses, or whatever: one or more underscores at the beginning: _refrobnicate_data_tables(), _destroy_cache().  

// Types of parameter:    
//  Parameter: 1  +   (host, nu_id) or (-p, port_number, host, nu_id), or ( -s, host, nu_id) or (-p, port_number, -s, host, nu_id)
// 1 + 2 or 4 or 3 or 5
    if(parameterCount==6&&parametersValidation(6,parameters)){
    // if(parameterCount == 6&&strncmp(parameters[1],"-p",2)==0 && strncmp(parameters[3],"-s",2)==0) {
        //printf("pass!\n");
        // use strtol instead of atoi
        port = strtol(parameters[2],NULL,10);
        // printf("port is: %i\n", port);
        ssl_flag = 1;
        strcat(parameters[5], theTerminator);
        strcat(info, parameters[5]);
    //}else if(parameterCount == 5&&strncmp(parameters[1],"-p",2)==0) {
    }else if(parameterCount==5&&parametersValidation(5,parameters)){
        port = strtol(parameters[2],NULL,10);
        //printf("port is: %i\n",port );
        strcat(parameters[4], theTerminator);
        strcat(info, parameters[4]);
        // printf("yes it's 5\n");
    //}else if(parameterCount == 4) {
    }else if(parameterCount==4&&parametersValidation(4,parameters)){
        port = DEFAULT_SSL_PORT;
        strcat(parameters[3], theTerminator);
        strcat(info, parameters[3]);
        ssl_flag = 1;
    //}else if(parameterCount == 3) {
    }else if(parameterCount==3&&parametersValidation(3,parameters)){
        port = DEFAULT_PORT;
        //printf("parameters1 before strcat: %s\n",parameters[1] );
        strcat(parameters[2], theTerminator);
        //printf("parameters1 after strcat: %s\n",parameters[1] );
        //printf("checker.\n");
        strcat(info, parameters[2]);
        //printf("info at last: %s\n",info );
    }else {
        //printf("parameters wrong.\n");
        errorHandler("Error: Wrong parameters. Use format: <-p port> <-s> [hostname] [NEU ID]");
    }

    // int i;
    // for(i=0;i<parameterCount;i++){
    //     printf("%s\n",parameters[i]);
    // }
    // printf("info: %s\n",info);
    // printf("parameters1: %s\n",parameters[1]);
    // printf("parameters4: %s\n",parameters[4]);
    // printf("test end\n");
    
    socketFileDescriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (socketFileDescriptor < 0){
        errorHandler("ERROR opening socket");
    }
    
    // if(parameterCount==6){
    // printf("host name length: %i\n", (int)strlen(parameters[parameterCount-2]));
    // char *c[] = parameters[parameterCount-2];
    // printf("c array is: %s\n", *c);
    // printf("gethostbyname with: %s\n",parameters[parameterCount-2]);
    // char *host = "cs5700.ccs.neu.edu";
    if ((h=gethostbyname(parameters[parameterCount-2])) == NULL){
        errorHandler("ERROR getting host");
    }
    // }
    // else if(parameterCount ==5){
    //     if ((h=gethostbyname(parameters[3])) == NULL)  
    //     errorHandler("ERROR getting host");
    // }else if(parameterCount == 3){
    //     if ((h=gethostbyname(parameters[1])) == NULL)  
    //             errorHandler("ERROR getting host");
    // }
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET; 
    server_addr.sin_port = htons(port);
    bcopy((char *)h->h_addr,
        (char *)&server_addr.sin_addr.s_addr,
          h->h_length);
    //printf("socketFileDescriptor: %i\n",socketFileDescriptor);
    //int size = sizeof(server_addr);
    //printf("sizeof(server_addr): %i\n",size);
    if (connect(socketFileDescriptor,(struct sockaddr *) &server_addr,sizeof(server_addr)) < 0){
        errorHandler("ERROR connecting");
    }
 
    if(ssl_flag == 1){
        SSLConnection(socketFileDescriptor, info);
    }
    else{
        // printf("non ssl process.\n");
        // printf("info: %s\n", info);
        normalConnection(socketFileDescriptor, info);
    }
    close(socketFileDescriptor);

    return 0;
}
