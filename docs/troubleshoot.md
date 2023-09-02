## Device select
```bash
# Check device number
arecord -l

# Max volume
amixer -c 2 set 'Capture' 100%


# Record example
# 2,0 card number, device number
arecord -D "plughw:2,0" -f S16_LE -r 16000 -d 5 -t wav data/test.wav


```
