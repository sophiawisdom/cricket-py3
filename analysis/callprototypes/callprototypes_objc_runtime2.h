typedef void *      __builtin_va_list;


typedef signed char __int8_t;
typedef unsigned char __uint8_t;
typedef short __int16_t;
typedef unsigned short __uint16_t;
typedef int __int32_t;
typedef unsigned int __uint32_t;
typedef long long __int64_t;
typedef unsigned long long __uint64_t;
typedef long __darwin_intptr_t;
typedef unsigned int __darwin_natural_t;
typedef int __darwin_ct_rune_t;
typedef union {
 char __mbstate8[128];
 long long _mbstateL;
} __mbstate_t;
typedef __mbstate_t __darwin_mbstate_t;
typedef long int __darwin_ptrdiff_t;
typedef long unsigned int __darwin_size_t;
typedef __builtin_va_list __darwin_va_list;
typedef int __darwin_wchar_t;
typedef __darwin_wchar_t __darwin_rune_t;
typedef int __darwin_wint_t;
typedef unsigned long __darwin_clock_t;
typedef __uint32_t __darwin_socklen_t;
typedef long __darwin_ssize_t;
typedef long __darwin_time_t;
typedef signed char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef long long int64_t;
typedef unsigned char u_int8_t;
typedef unsigned short u_int16_t;
typedef unsigned int u_int32_t;
typedef unsigned long long u_int64_t;
typedef int64_t register_t;
typedef __darwin_intptr_t intptr_t;
typedef unsigned long uintptr_t;
typedef u_int64_t user_addr_t;
typedef u_int64_t user_size_t;
typedef int64_t user_ssize_t;
typedef int64_t user_long_t;
typedef u_int64_t user_ulong_t;
typedef int64_t user_time_t;
typedef int64_t user_off_t;
typedef u_int64_t syscall_arg_t;
typedef __int64_t __darwin_blkcnt_t;
typedef __int32_t __darwin_blksize_t;
typedef __int32_t __darwin_dev_t;
typedef unsigned int __darwin_fsblkcnt_t;
typedef unsigned int __darwin_fsfilcnt_t;
typedef __uint32_t __darwin_gid_t;
typedef __uint32_t __darwin_id_t;
typedef __uint64_t __darwin_ino64_t;
typedef __darwin_ino64_t __darwin_ino_t;
typedef __darwin_natural_t __darwin_mach_port_name_t;
typedef __darwin_mach_port_name_t __darwin_mach_port_t;
typedef __uint16_t __darwin_mode_t;
typedef __int64_t __darwin_off_t;
typedef __int32_t __darwin_pid_t;
typedef __uint32_t __darwin_sigset_t;
typedef __int32_t __darwin_suseconds_t;
typedef __uint32_t __darwin_uid_t;
typedef __uint32_t __darwin_useconds_t;
typedef unsigned char __darwin_uuid_t[16];
typedef char __darwin_uuid_string_t[37];
struct __darwin_pthread_handler_rec {
 void (*__routine)(void *);
 void *__arg;
 struct __darwin_pthread_handler_rec *__next;
};
struct _opaque_pthread_attr_t {
 long __sig;
 char __opaque[56];
};
struct _opaque_pthread_cond_t {
 long __sig;
 char __opaque[40];
};
struct _opaque_pthread_condattr_t {
 long __sig;
 char __opaque[8];
};
struct _opaque_pthread_mutex_t {
 long __sig;
 char __opaque[56];
};
struct _opaque_pthread_mutexattr_t {
 long __sig;
 char __opaque[8];
};
struct _opaque_pthread_once_t {
 long __sig;
 char __opaque[8];
};
struct _opaque_pthread_rwlock_t {
 long __sig;
 char __opaque[192];
};
struct _opaque_pthread_rwlockattr_t {
 long __sig;
 char __opaque[16];
};
struct _opaque_pthread_t {
 long __sig;
 struct __darwin_pthread_handler_rec *__cleanup_stack;
 char __opaque[8176];
};
typedef struct _opaque_pthread_attr_t __darwin_pthread_attr_t;
typedef struct _opaque_pthread_cond_t __darwin_pthread_cond_t;
typedef struct _opaque_pthread_condattr_t __darwin_pthread_condattr_t;
typedef unsigned long __darwin_pthread_key_t;
typedef struct _opaque_pthread_mutex_t __darwin_pthread_mutex_t;
typedef struct _opaque_pthread_mutexattr_t __darwin_pthread_mutexattr_t;
typedef struct _opaque_pthread_once_t __darwin_pthread_once_t;
typedef struct _opaque_pthread_rwlock_t __darwin_pthread_rwlock_t;
typedef struct _opaque_pthread_rwlockattr_t __darwin_pthread_rwlockattr_t;
typedef struct _opaque_pthread_t *__darwin_pthread_t;
typedef unsigned char u_char;
typedef unsigned short u_short;
typedef unsigned int u_int;
typedef unsigned long u_long;
typedef unsigned short ushort;
typedef unsigned int uint;
typedef u_int64_t u_quad_t;
typedef int64_t quad_t;
typedef quad_t * qaddr_t;
typedef char * caddr_t;
typedef int32_t daddr_t;
typedef __darwin_dev_t dev_t;
typedef u_int32_t fixpt_t;
typedef __darwin_blkcnt_t blkcnt_t;
typedef __darwin_blksize_t blksize_t;
typedef __darwin_gid_t gid_t;
typedef __uint32_t in_addr_t;
typedef __uint16_t in_port_t;
typedef __darwin_ino_t ino_t;
typedef __darwin_ino64_t ino64_t;
typedef __int32_t key_t;
typedef __darwin_mode_t mode_t;
typedef __uint16_t nlink_t;
typedef __darwin_id_t id_t;
typedef __darwin_pid_t pid_t;
typedef __darwin_off_t off_t;
typedef int32_t segsz_t;
typedef int32_t swblk_t;
typedef __darwin_uid_t uid_t;
typedef __darwin_clock_t clock_t;
typedef __darwin_size_t size_t;
typedef __darwin_ssize_t ssize_t;
typedef __darwin_time_t time_t;
typedef __darwin_useconds_t useconds_t;
typedef __darwin_suseconds_t suseconds_t;
typedef __darwin_size_t rsize_t;
typedef int errno_t;
typedef struct fd_set {
 __int32_t fds_bits[((((1024) % ((sizeof(__int32_t) * 8))) == 0) ? ((1024) / ((sizeof(__int32_t) * 8))) : (((1024) / ((sizeof(__int32_t) * 8))) + 1))];
} fd_set;
typedef __int32_t fd_mask;
typedef __darwin_pthread_attr_t pthread_attr_t;
typedef __darwin_pthread_cond_t pthread_cond_t;
typedef __darwin_pthread_condattr_t pthread_condattr_t;
typedef __darwin_pthread_mutex_t pthread_mutex_t;
typedef __darwin_pthread_mutexattr_t pthread_mutexattr_t;
typedef __darwin_pthread_once_t pthread_once_t;
typedef __darwin_pthread_rwlock_t pthread_rwlock_t;
typedef __darwin_pthread_rwlockattr_t pthread_rwlockattr_t;
typedef __darwin_pthread_t pthread_t;
typedef __darwin_pthread_key_t pthread_key_t;
typedef __darwin_fsblkcnt_t fsblkcnt_t;
typedef __darwin_fsfilcnt_t fsfilcnt_t;
typedef struct objc_class *Class;
struct objc_object {
    Class isa ;
};
typedef struct objc_object *id;
typedef struct objc_selector *SEL;
typedef id (*IMP)(id, SEL, ...);
typedef signed char BOOL;
const char *sel_getName(SEL sel)
    ;
SEL sel_registerName(const char *str)
    ;
const char *object_getClassName(id obj)
    ;
void *object_getIndexedIvars(id obj)
    ;
BOOL sel_isMapped(SEL sel)
    ;
SEL sel_getUid(const char *str)
    ;
typedef const void* objc_objectptr_t;
    typedef long arith_t;
    typedef unsigned long uarith_t;
typedef char *STR;
typedef __builtin_va_list va_list;
typedef __builtin_va_list __gnuc_va_list;
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;
typedef int8_t int_least8_t;
typedef int16_t int_least16_t;
typedef int32_t int_least32_t;
typedef int64_t int_least64_t;
typedef uint8_t uint_least8_t;
typedef uint16_t uint_least16_t;
typedef uint32_t uint_least32_t;
typedef uint64_t uint_least64_t;
typedef int8_t int_fast8_t;
typedef int16_t int_fast16_t;
typedef int32_t int_fast32_t;
typedef int64_t int_fast64_t;
typedef uint8_t uint_fast8_t;
typedef uint16_t uint_fast16_t;
typedef uint32_t uint_fast32_t;
typedef uint64_t uint_fast64_t;
typedef long int intmax_t;
typedef long unsigned int uintmax_t;
typedef long int ptrdiff_t;
typedef int wchar_t;
typedef struct objc_method *Method;
typedef struct objc_ivar *Ivar;
typedef struct objc_category *Category;
typedef struct objc_property *objc_property_t;
struct objc_class {
    Class isa ;
    Class super_class ;
    const char *name ;
    long version ;
    long info ;
    long instance_size ;
    struct objc_ivar_list *ivars ;
    struct objc_method_list **methodLists ;
    struct objc_cache *cache ;
    struct objc_protocol_list *protocols ;
} ;
typedef struct objc_object Protocol;
struct objc_method_description {
 SEL name;
 char *types;
};
typedef struct {
    const char *name;
    const char *value;
} objc_property_attribute_t;
id object_copy(id obj, size_t size)

                        ;
id object_dispose(id obj)

                        ;
Class object_getClass(id obj)
     ;
Class object_setClass(id obj, Class cls)
     ;
BOOL object_isClass(id obj)
    ;
const char *object_getClassName(id obj)
    ;
void *object_getIndexedIvars(id obj)

                        ;
id object_getIvar(id obj, Ivar ivar)
     ;
void object_setIvar(id obj, Ivar ivar, id value)
     ;
Ivar object_setInstanceVariable(id obj, const char *name, void *value)

                        ;
Ivar object_getInstanceVariable(id obj, const char *name, void **outValue)

                        ;
Class objc_getClass(const char *name)
    ;
Class objc_getMetaClass(const char *name)
    ;
Class objc_lookUpClass(const char *name)
    ;
Class objc_getRequiredClass(const char *name)
    ;
int objc_getClassList(Class *buffer, int bufferCount)
    ;
Class *objc_copyClassList(unsigned int *outCount)
     ;
const char *class_getName(Class cls)
     ;
BOOL class_isMetaClass(Class cls)
     ;
Class class_getSuperclass(Class cls)
     ;
Class class_setSuperclass(Class cls, Class newSuper)
     ;
int class_getVersion(Class cls)
    ;
void class_setVersion(Class cls, int version)
    ;
size_t class_getInstanceSize(Class cls)
     ;
Ivar class_getInstanceVariable(Class cls, const char *name)
    ;
Ivar class_getClassVariable(Class cls, const char *name)
     ;
Ivar *class_copyIvarList(Class cls, unsigned int *outCount)
     ;
Method class_getInstanceMethod(Class cls, SEL name)
    ;
Method class_getClassMethod(Class cls, SEL name)
    ;
IMP class_getMethodImplementation(Class cls, SEL name)
     ;
IMP class_getMethodImplementation_stret(Class cls, SEL name)

                           ;
BOOL class_respondsToSelector(Class cls, SEL sel)
     ;
Method *class_copyMethodList(Class cls, unsigned int *outCount)
     ;
BOOL class_conformsToProtocol(Class cls, Protocol *protocol)
     ;
Protocol * *class_copyProtocolList(Class cls, unsigned int *outCount)
     ;
objc_property_t class_getProperty(Class cls, const char *name)
     ;
objc_property_t *class_copyPropertyList(Class cls, unsigned int *outCount)
     ;
const uint8_t *class_getIvarLayout(Class cls)
     ;
const uint8_t *class_getWeakIvarLayout(Class cls)
     ;
BOOL class_addMethod(Class cls, SEL name, IMP imp,
                                 const char *types)
     ;
IMP class_replaceMethod(Class cls, SEL name, IMP imp,
                                    const char *types)
     ;
BOOL class_addIvar(Class cls, const char *name, size_t size,
                               uint8_t alignment, const char *types)
     ;
BOOL class_addProtocol(Class cls, Protocol *protocol)
     ;
BOOL class_addProperty(Class cls, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount)
     ;
void class_replaceProperty(Class cls, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount)
     ;
void class_setIvarLayout(Class cls, const uint8_t *layout)
     ;
void class_setWeakIvarLayout(Class cls, const uint8_t *layout)
     ;
Class objc_getFutureClass(const char *name)

                         ;
void objc_setFutureClass(Class cls, const char *name)

                         ;
id class_createInstance(Class cls, size_t extraBytes)

                        ;
id objc_constructInstance(Class cls, void *bytes)

                        ;
void *objc_destructInstance(id obj)

                        ;
Class objc_allocateClassPair(Class superclass, const char *name,
                                         size_t extraBytes)
     ;
void objc_registerClassPair(Class cls)
     ;
Class objc_duplicateClass(Class original, const char *name, size_t extraBytes)
     ;
void objc_disposeClassPair(Class cls)
     ;
SEL method_getName(Method m)
     ;
IMP method_getImplementation(Method m)
     ;
const char *method_getTypeEncoding(Method m)
     ;
unsigned int method_getNumberOfArguments(Method m)
    ;
char *method_copyReturnType(Method m)
     ;
char *method_copyArgumentType(Method m, unsigned int index)
     ;
void method_getReturnType(Method m, char *dst, size_t dst_len)
     ;
void method_getArgumentType(Method m, unsigned int index,
                                        char *dst, size_t dst_len)
     ;
struct objc_method_description *method_getDescription(Method m)
     ;
IMP method_setImplementation(Method m, IMP imp)
     ;
void method_exchangeImplementations(Method m1, Method m2)
     ;
const char *ivar_getName(Ivar v)
     ;
const char *ivar_getTypeEncoding(Ivar v)
     ;
ptrdiff_t ivar_getOffset(Ivar v)
     ;
const char *property_getName(objc_property_t property)
     ;
const char *property_getAttributes(objc_property_t property)
     ;
objc_property_attribute_t *property_copyAttributeList(objc_property_t property, unsigned int *outCount)
     ;
char *property_copyAttributeValue(objc_property_t property, const char *attributeName)
     ;
Protocol *objc_getProtocol(const char *name)
     ;
Protocol * *objc_copyProtocolList(unsigned int *outCount)
     ;
BOOL protocol_conformsToProtocol(Protocol *proto, Protocol *other)
     ;
BOOL protocol_isEqual(Protocol *proto, Protocol *other)
     ;
const char *protocol_getName(Protocol *p)
     ;
struct objc_method_description protocol_getMethodDescription(Protocol *p, SEL aSel, BOOL isRequiredMethod, BOOL isInstanceMethod)
     ;
struct objc_method_description *protocol_copyMethodDescriptionList(Protocol *p, BOOL isRequiredMethod, BOOL isInstanceMethod, unsigned int *outCount)
     ;
objc_property_t protocol_getProperty(Protocol *proto, const char *name, BOOL isRequiredProperty, BOOL isInstanceProperty)
     ;
objc_property_t *protocol_copyPropertyList(Protocol *proto, unsigned int *outCount)
     ;
Protocol * *protocol_copyProtocolList(Protocol *proto, unsigned int *outCount)
     ;
Protocol *objc_allocateProtocol(const char *name)
     ;
void objc_registerProtocol(Protocol *proto)
     ;
void protocol_addMethodDescription(Protocol *proto, SEL name, const char *types, BOOL isRequiredMethod, BOOL isInstanceMethod)
     ;
void protocol_addProtocol(Protocol *proto, Protocol *addition)
     ;
void protocol_addProperty(Protocol *proto, const char *name, const objc_property_attribute_t *attributes, unsigned int attributeCount, BOOL isRequiredProperty, BOOL isInstanceProperty)
     ;
const char **objc_copyImageNames(unsigned int *outCount)
     ;
const char *class_getImageName(Class cls)
     ;
const char **objc_copyClassNamesForImage(const char *image,
                                                     unsigned int *outCount)
     ;
const char *sel_getName(SEL sel)
    ;
SEL sel_getUid(const char *str)
    ;
SEL sel_registerName(const char *str)
    ;
BOOL sel_isEqual(SEL lhs, SEL rhs)
     ;
void objc_enumerationMutation(id obj)
     ;
void objc_setEnumerationMutationHandler(void (*handler)(id))
     ;
void objc_setForwardHandler(void *fwd, void *fwd_stret)
     ;
IMP imp_implementationWithBlock(id block)
     ;
id imp_getBlock(IMP anImp)
     ;
BOOL imp_removeBlock(IMP anImp)
     ;
id objc_loadWeak(id *location)
    ;
id objc_storeWeak(id *location, id obj)
    ;
enum {
    OBJC_ASSOCIATION_ASSIGN = 0,
    OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1,
    OBJC_ASSOCIATION_COPY_NONATOMIC = 3,
    OBJC_ASSOCIATION_RETAIN = 01401,
    OBJC_ASSOCIATION_COPY = 01403
};
typedef uintptr_t objc_AssociationPolicy;
void objc_setAssociatedObject(id object, const void *key, id value, objc_AssociationPolicy policy)
    ;
id objc_getAssociatedObject(id object, const void *key)
    ;
void objc_removeAssociatedObjects(id object)
    ;
struct objc_method_description_list {
        int count;
        struct objc_method_description list[1];
};
struct objc_protocol_list {
    struct objc_protocol_list *next;
    long count;
    Protocol *list[1];
};
struct objc_category {
    char *category_name ;
    char *class_name ;
    struct objc_method_list *instance_methods ;
    struct objc_method_list *class_methods ;
    struct objc_protocol_list *protocols ;
} ;
struct objc_ivar {
    char *ivar_name ;
    char *ivar_type ;
    int ivar_offset ;
    int space ;
} ;
struct objc_ivar_list {
    int ivar_count ;
    int space ;
    struct objc_ivar ivar_list[1] ;
} ;
struct objc_method {
    SEL method_name ;
    char *method_types ;
    IMP method_imp ;
} ;
struct objc_method_list {
    struct objc_method_list *obsolete ;
    int method_count ;
    int space ;
    struct objc_method method_list[1] ;
} ;
typedef struct objc_symtab *Symtab ;
struct objc_symtab {
    unsigned long sel_ref_cnt ;
    SEL *refs ;
    unsigned short cls_def_cnt ;
    unsigned short cat_def_cnt ;
    void *defs[1] ;
} ;
typedef struct objc_cache *Cache ;
struct objc_cache {
    unsigned int mask ;
    unsigned int occupied ;
    Method buckets[1] ;
};
typedef struct objc_module *Module ;
struct objc_module {
    unsigned long version ;
    unsigned long size ;
    const char *name ;
    Symtab symtab ;
} ;
IMP class_lookupMethod(Class cls, SEL sel)
    ;
BOOL class_respondsToMethod(Class cls, SEL sel)
    ;
void _objc_flush_caches(Class cls)
    ;
id object_copyFromZone(id anObject, size_t nBytes, void *z)

                        ;
id object_realloc(id anObject, size_t nBytes) ;
id object_reallocFromZone(id anObject, size_t nBytes, void *z) ;
void *objc_getClasses(void) ;
void objc_addClass(Class myClass) ;
void objc_setClassHandler(int (*)(const char *)) ;
void objc_setMultithreaded (BOOL flag) ;
id class_createInstanceFromZone(Class, size_t idxIvars, void *z)

                        ;
void class_addMethods(Class, struct objc_method_list *) ;
void class_removeMethods(Class, struct objc_method_list *) ;
void _objc_resolve_categories_for_class(Class cls) ;
Class class_poseAs(Class imposter, Class original) ;
unsigned int method_getSizeOfArguments(Method m) ;
unsigned method_getArgumentInfo(struct objc_method *m, int arg, const char **type, int *offset) ;
Class objc_getOrigClass(const char *name) ;
struct objc_method_list *class_nextMethodList(Class, void **) ;
id (*_alloc)(Class, size_t) ;
id (*_copy)(id, size_t) ;
id (*_realloc)(id, size_t) ;
id (*_dealloc)(id) ;
id (*_zoneAlloc)(Class, size_t, void *) ;
id (*_zoneRealloc)(id, size_t, void *) ;
id (*_zoneCopy)(id, size_t, void *) ;
void (*_error)(id, const char *, va_list) ;
