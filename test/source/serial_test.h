#ifndef _SERIAL_H_
#define	_SERIAL_H_

#ifdef	__cplusplus
extern "C" {
#endif
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <unistd.h>

#define BUFLEN 6500

char buffer[BUFLEN];


int   serialOpen(const char* device, const int baud);
void  serialClose(const int fd);
void  serialFlush(const int fd);
void  serialPutchar(const int fd, const unsigned char c);
void  serialPuts(const int fd, unsigned char* s);
void  serialPrintf(const int fd, const char* message, ...);
void serialPrint(const int fd, unsigned char* message);
int   serialDataAvail(const int fd);
int   serialGetchar(const int fd);

void send(const int fd, unsigned char* buf, unsigned int len);
char* readfrom(const int fd, char stop, int pause);
char* readdata(const int fd, char stop, int pause, int buflen);


#ifdef	__cplusplus
}
#endif

#endif	/* _SERIAL_H_ */

