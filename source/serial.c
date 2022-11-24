

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
#include <malloc.h>
#include <stdbool.h>
#include "wiringPi.h"
#include "serial.h"
//#include "wiringSerial.h"
/*
 * serialOpen:
 *	Open and initialise the serial port, setting all the right
 *	port parameters - or as many as are required - hopefully!
 *********************************************************************************
 */




int serialOpen(const char* device, const int baud)
{
    struct termios options;
    speed_t myBaud;
    int     status, fd;

    switch (baud)
    {
    case      50:	myBaud = B50; break;
    case      75:	myBaud = B75; break;
    case     110:	myBaud = B110; break;
    case     134:	myBaud = B134; break;
    case     150:	myBaud = B150; break;
    case     200:	myBaud = B200; break;
    case     300:	myBaud = B300; break;
    case     600:	myBaud = B600; break;
    case    1200:	myBaud = B1200; break;
    case    1800:	myBaud = B1800; break;
    case    2400:	myBaud = B2400; break;
    case    4800:	myBaud = B4800; break;
    case    9600:	myBaud = B9600; break;
    case   19200:	myBaud = B19200; break;
    case   38400:	myBaud = B38400; break;
    case   57600:	myBaud = B57600; break;
    case  115200:	myBaud = B115200; break;
    case  230400:	myBaud = B230400; break;
    case  460800:	myBaud = B460800; break;
    case  500000:	myBaud = B500000; break;
    case  576000:	myBaud = B576000; break;
    case  921600:	myBaud = B921600; break;
    case 1000000:	myBaud = B1000000; break;
    case 1152000:	myBaud = B1152000; break;
    case 1500000:	myBaud = B1500000; break;
    case 2000000:	myBaud = B2000000; break;
    case 2500000:	myBaud = B2500000; break;
    case 3000000:	myBaud = B3000000; break;
    case 3500000:	myBaud = B3500000; break;
    case 4000000:	myBaud = B4000000; break;

    default:
        return -2;
    }

    if ((fd = open(device, O_RDWR | O_NOCTTY | O_NONBLOCK | O_NDELAY)) == -1)// 
        return -1;

    fcntl(fd, F_SETFL, O_RDWR);

    // Get and modify current options:

    tcgetattr(fd, &options);

    cfmakeraw(&options);
    cfsetispeed(&options, myBaud);
    cfsetospeed(&options, myBaud);

    options.c_cflag |= (CLOCAL | CREAD);
    options.c_cflag &= ~PARENB;
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    options.c_oflag &= ~OPOST;

    options.c_cc[VMIN] = 0;
    options.c_cc[VTIME] = 100; // Ten seconds (100 deciseconds)

    tcsetattr(fd, TCSANOW, &options);

    ioctl(fd, TIOCMGET, &status);

    status |= TIOCM_DTR;
    status |= TIOCM_RTS;

    ioctl(fd, TIOCMSET, &status);

    usleep(10000); // 10mS


    return fd;
}


/*
 * serialFlush:
 *	Flush the serial buffers (both tx & rx)
 *********************************************************************************
 */

void serialFlush(const int fd)
{
    tcflush(fd, TCIOFLUSH);
}


/*
 * serialClose:
 *	Release the serial port
 *********************************************************************************
 */

void serialClose(const int fd)
{
    close(fd);
}


/*
 * serialPutchar:
 *	Send a single character to the serial port
 *********************************************************************************
 */

void serialPutchar(const int fd, const unsigned char c)
{
    write(fd, &c, 1);
}


/*
 * serialPuts:
 *	Send a string to the serial port
 *********************************************************************************
 */

void serialPuts(const int fd, unsigned char* s)
{
    write(fd, (const unsigned char*) s, strlen(s));
}

/*
 * serialPrintf:
 *	Printf over Serial
 *********************************************************************************
 */

void serialPrintf(const int fd, const char* message, ...)
{
    va_list argp;
    char buffer[1024];

    va_start(argp, message);
    vsnprintf(buffer, 1023, message, argp);
    va_end(argp);

    serialPuts(fd, buffer);
}

void serialPrint(const int fd, unsigned char* message)
{
    //if (!serialDataAvail(fd))serialFlush(fd);
    serialPuts(fd, message);
    fflush(stdout);
}



/*
 * serialDataAvail:
 *	Return the number of bytes of data avalable to be read in the serial port
 *********************************************************************************
 */

int serialDataAvail(const int fd)
{
    int result;

    if (ioctl(fd, FIONREAD, &result) == -1)
        return -1;

    return result;
}

/*
 * serialGetchar:
 *	Get a single character from the serial device.
 *	Note: Zero is a valid character and this function will time-out after
 *	10 seconds.
 *********************************************************************************
 */

int serialGetchar(const int fd)
{
    uint8_t x;

    if (read(fd, &x, 1) != 1)
        return -1;

    return ((int)x) & 0xFF;
}



void send(const int fd, unsigned char  *buf, unsigned int len) {
    //if (!serialDataAvail(fd))serialFlush(fd);
    for (unsigned int i = 0; i < len; i++)
        serialPutchar(fd, (const unsigned char)buf[i]);
    fflush(stdout);
}


char* readfrom(const int fd,char stop,int pause) {
    int count = 0;
    int dat;
    unsigned long time = millis();
    memset(buffer, '\0', BUFLEN);
    //int st = -1;
    
    while (millis()< time+ pause) {

        if (serialDataAvail(fd) && serialDataAvail(fd) != -1) {
            dat = serialGetchar(fd);
            buffer[count] = dat;
            count++;
            
            if (dat == (int)stop) {
                
                count = 0;
               
                serialFlush(fd);
               
                break;
            }
            else if (count > BUFLEN) {
              
                serialFlush(fd);
                break;
            }

        }

    }
    return buffer;
}

char* readdata(const int fd, char stop, int pause, int buflen)

{
    int count = 0;
    int dat;
    unsigned long time = millis();
    memset(buffer, '\0', BUFLEN);
    
    char *bufs = (char*)malloc(buflen * sizeof(char));
   
    //int st = -1;
    while (millis() < time + pause && count < buflen) {

        if (serialDataAvail(fd) && serialDataAvail(fd) != -1) {
            dat = serialGetchar(fd);
            bufs[count] = dat;
            count++;
            fflush(stdout);
        }
        if (count > BUFLEN) {

            serialFlush(fd);
            break;
        }


    }
    serialFlush(fd);
    bool state = 0;
    int index = 0;
    for (int i = 0; i < count; i++) {
        if (state) {
            buffer[index] = bufs[i];
            if (bufs[i] == stop) break;
            index++;
        }
        if (bufs[i] == stop) state = 1;

    }
    free(bufs);
    return buffer;

}