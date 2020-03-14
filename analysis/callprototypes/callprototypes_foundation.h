typedef void * id;

void NSLog(id format, ...);
int printf(const char * __restrict, ...);

typedef void * CFTypeRef;
CFTypeRef CFRetain(CFTypeRef cf);
void CFRelease(CFTypeRef cf);


id CFRunLoopGetTypeID(void);
id CFRunLoopGetCurrent(void);
id CFRunLoopGetMain(void);

id CFRunLoopCopyCurrentMode(id rl);

id CFRunLoopCopyAllModes(id rl);

void CFRunLoopAddCommonMode(id rl, id mode);

void CFRunLoopRun(void);
void CFRunLoopWakeUp(id rl);
void CFRunLoopStop(id rl);
