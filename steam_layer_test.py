from pylsl import StreamInfo, StreamOutlet, local_clock
from random import random as rand
import time

srate = 100
name = 'pi-top chan'
ttype = 'Thermal'
n_channels = 8
info = StreamInfo(name, ttype, n_channels, srate, 'float32', 'myuid34234')
outlet = StreamOutlet(info)

print("now sending data...")
start_time = local_clock()
sent_samples = 0
while True:
    elapsed_time = local_clock() - start_time
    required_samples = int(srate * elapsed_time) - sent_samples
    for sample_ix in range(required_samples):
        # make a new random n_channels sample; this is converted into a
        # pylsl.vectorf (the data type that is expected by push_sample)
        # now send it
        outlet.push_sample(mysample)
    sent_samples += required_samples
    # now send it and wait for a bit before trying again.
    time.sleep(0.01)