#include "linux/fs.h"
#include "linux/cdev.h"
#include "linux/module.h"
#include "linux/kernel.h"
#include "linux/delay.h"
#include "linux/kthread.h"
#include "linux/device.h"
#include "linux/slab.h"
#include "linux/tty.h"
#include "linux/tty_flip.h"
#include "linux/kbd_kern.h"
#include "linux/input.h"

/* vtkbd kernel thread struct */
static struct task_struct *vtkbd_thread_task;

/* vtkbd input device structure */
static struct input_dev *vtkbd_input_dev;

const char str_keys[] = { KEY_S, KEY_E, KEY_G, KEY_M, KEY_E, KEY_N,
                          KEY_T, KEY_A, KEY_T, KEY_I, KEY_O, KEY_N,
                          KEY_SPACE, KEY_F, KEY_A, KEY_U, KEY_L,
                          KEY_T, KEY_ENTER };

/* kernel thread */
static int vtkbd_thread(void *unused)
{
    int i;

    while (!kthread_should_stop()) {

        for (i = 0; i < sizeof(str_keys); i++) {

            input_report_key(vtkbd_input_dev, str_keys[i], 1);
            input_report_key(vtkbd_input_dev, str_keys[i], 0);
            input_sync(vtkbd_input_dev);

        }

        /* wait 10 seconds */
        msleep(10000);
    }

    return(0);
}

/* driver initialization */
static int __init vtkbd_init(void)
{
    static const char *name = "Virtual Keyboard";
    int i;

    /* allocate input device */
    vtkbd_input_dev = input_allocate_device();
    if (!vtkbd_input_dev) {
        printk("vtkbd_init: Error on input_allocate_device!\n");
        return -ENOMEM;
    }

    /* set input device name */
    vtkbd_input_dev->name = name;

    /* enable key events */
    set_bit(EV_KEY, vtkbd_input_dev->evbit);
    for (i = 0; i < 256; i++)
        set_bit(i, vtkbd_input_dev->keybit);

    /* register input device */
    input_register_device(vtkbd_input_dev);

    /* start thread */
    vtkbd_thread_task = kthread_run(vtkbd_thread, NULL, "%s", "vtkbd_thread");

    printk("Virtual Keyboard driver initialized.\n");

    return 0;
}

/* driver exit */
void __exit vtkbd_exit(void)
{
    /* stop thread */
    kthread_stop(vtkbd_thread_task);

    /* unregister input device */
    input_unregister_device(vtkbd_input_dev);

        ("Virtual Keyboard driver.\n");
}

module_init(vtkbd_init);
module_exit(vtkbd_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Sergio Prado sergio.prado@embeddedlabworks.com");
MODULE_DESCRIPTION("Virtual Keyboard driver");
