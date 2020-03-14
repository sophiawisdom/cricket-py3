typedef void * id;
typedef char * SEL;
typedef long ptrdiff_t;
typedef unsigned char BOOL;

id objc_autorelease(id value);
void objc_autoreleasePoolPop(void *pool);
void *objc_autoreleasePoolPush(void);
id objc_autoreleaseReturnValue(id value);
void objc_copyWeak(id *dest, id *src);
void objc_destroyWeak(id *object);
id objc_initWeak(id *object, id value);
id objc_loadWeak(id *object);
id objc_loadWeakRetained(id *object);
void objc_moveWeak(id *dest, id *src);
void objc_release(id value);
id objc_retain(id value);
id objc_retainAutorelease(id value);
id objc_retainAutoreleaseReturnValue(id value);
id objc_retainAutoreleasedReturnValue(id value);
id objc_retainBlock(id value);
id objc_storeStrong(id *object, id value);
id objc_storeWeak(id *object, id value);

id objc_getProperty(id self, SEL _cmd, ptrdiff_t offset, BOOL atomic);
void objc_setProperty(id self, SEL _cmd, ptrdiff_t offset, id newValue, BOOL atomic, signed char shouldCopy);
void objc_setProperty_atomic(id self, SEL _cmd, id newValue, ptrdiff_t offset);
void objc_setProperty_nonatomic(id self, SEL _cmd, id newValue, ptrdiff_t offset);
void objc_setProperty_atomic_copy(id self, SEL _cmd, id newValue, ptrdiff_t offset);
void objc_setProperty_nonatomic_copy(id self, SEL _cmd, id newValue, ptrdiff_t offset);

id objc_msgSend(id self, SEL op, ...);
id objc_msgSendSuper(id super, SEL op, ...);
id objc_msgSendSuper2(id super, SEL op, ...);
