typedef void *      __builtin_va_list;


typedef int sig_atomic_t;
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
struct __darwin_i386_thread_state
{
    unsigned int __eax;
    unsigned int __ebx;
    unsigned int __ecx;
    unsigned int __edx;
    unsigned int __edi;
    unsigned int __esi;
    unsigned int __ebp;
    unsigned int __esp;
    unsigned int __ss;
    unsigned int __eflags;
    unsigned int __eip;
    unsigned int __cs;
    unsigned int __ds;
    unsigned int __es;
    unsigned int __fs;
    unsigned int __gs;
};
struct __darwin_fp_control
{
    unsigned short __invalid :1,
        __denorm :1,
    __zdiv :1,
    __ovrfl :1,
    __undfl :1,
    __precis :1,
      :2,
    __pc :2,
    __rc :2,
             :1,
      :3;
};
typedef struct __darwin_fp_control __darwin_fp_control_t;
struct __darwin_fp_status
{
    unsigned short __invalid :1,
        __denorm :1,
    __zdiv :1,
    __ovrfl :1,
    __undfl :1,
    __precis :1,
    __stkflt :1,
    __errsumm :1,
    __c0 :1,
    __c1 :1,
    __c2 :1,
    __tos :3,
    __c3 :1,
    __busy :1;
};
typedef struct __darwin_fp_status __darwin_fp_status_t;
struct __darwin_mmst_reg
{
 char __mmst_reg[10];
 char __mmst_rsrv[6];
};
struct __darwin_xmm_reg
{
 char __xmm_reg[16];
};
struct __darwin_i386_float_state
{
 int __fpu_reserved[2];
 struct __darwin_fp_control __fpu_fcw;
 struct __darwin_fp_status __fpu_fsw;
 __uint8_t __fpu_ftw;
 __uint8_t __fpu_rsrv1;
 __uint16_t __fpu_fop;
 __uint32_t __fpu_ip;
 __uint16_t __fpu_cs;
 __uint16_t __fpu_rsrv2;
 __uint32_t __fpu_dp;
 __uint16_t __fpu_ds;
 __uint16_t __fpu_rsrv3;
 __uint32_t __fpu_mxcsr;
 __uint32_t __fpu_mxcsrmask;
 struct __darwin_mmst_reg __fpu_stmm0;
 struct __darwin_mmst_reg __fpu_stmm1;
 struct __darwin_mmst_reg __fpu_stmm2;
 struct __darwin_mmst_reg __fpu_stmm3;
 struct __darwin_mmst_reg __fpu_stmm4;
 struct __darwin_mmst_reg __fpu_stmm5;
 struct __darwin_mmst_reg __fpu_stmm6;
 struct __darwin_mmst_reg __fpu_stmm7;
 struct __darwin_xmm_reg __fpu_xmm0;
 struct __darwin_xmm_reg __fpu_xmm1;
 struct __darwin_xmm_reg __fpu_xmm2;
 struct __darwin_xmm_reg __fpu_xmm3;
 struct __darwin_xmm_reg __fpu_xmm4;
 struct __darwin_xmm_reg __fpu_xmm5;
 struct __darwin_xmm_reg __fpu_xmm6;
 struct __darwin_xmm_reg __fpu_xmm7;
 char __fpu_rsrv4[14*16];
 int __fpu_reserved1;
};
struct __darwin_i386_avx_state
{
 int __fpu_reserved[2];
 struct __darwin_fp_control __fpu_fcw;
 struct __darwin_fp_status __fpu_fsw;
 __uint8_t __fpu_ftw;
 __uint8_t __fpu_rsrv1;
 __uint16_t __fpu_fop;
 __uint32_t __fpu_ip;
 __uint16_t __fpu_cs;
 __uint16_t __fpu_rsrv2;
 __uint32_t __fpu_dp;
 __uint16_t __fpu_ds;
 __uint16_t __fpu_rsrv3;
 __uint32_t __fpu_mxcsr;
 __uint32_t __fpu_mxcsrmask;
 struct __darwin_mmst_reg __fpu_stmm0;
 struct __darwin_mmst_reg __fpu_stmm1;
 struct __darwin_mmst_reg __fpu_stmm2;
 struct __darwin_mmst_reg __fpu_stmm3;
 struct __darwin_mmst_reg __fpu_stmm4;
 struct __darwin_mmst_reg __fpu_stmm5;
 struct __darwin_mmst_reg __fpu_stmm6;
 struct __darwin_mmst_reg __fpu_stmm7;
 struct __darwin_xmm_reg __fpu_xmm0;
 struct __darwin_xmm_reg __fpu_xmm1;
 struct __darwin_xmm_reg __fpu_xmm2;
 struct __darwin_xmm_reg __fpu_xmm3;
 struct __darwin_xmm_reg __fpu_xmm4;
 struct __darwin_xmm_reg __fpu_xmm5;
 struct __darwin_xmm_reg __fpu_xmm6;
 struct __darwin_xmm_reg __fpu_xmm7;
 char __fpu_rsrv4[14*16];
 int __fpu_reserved1;
 char __avx_reserved1[64];
 struct __darwin_xmm_reg __fpu_ymmh0;
 struct __darwin_xmm_reg __fpu_ymmh1;
 struct __darwin_xmm_reg __fpu_ymmh2;
 struct __darwin_xmm_reg __fpu_ymmh3;
 struct __darwin_xmm_reg __fpu_ymmh4;
 struct __darwin_xmm_reg __fpu_ymmh5;
 struct __darwin_xmm_reg __fpu_ymmh6;
 struct __darwin_xmm_reg __fpu_ymmh7;
};
struct __darwin_i386_exception_state
{
 __uint16_t __trapno;
 __uint16_t __cpu;
 __uint32_t __err;
 __uint32_t __faultvaddr;
};
struct __darwin_x86_debug_state32
{
 unsigned int __dr0;
 unsigned int __dr1;
 unsigned int __dr2;
 unsigned int __dr3;
 unsigned int __dr4;
 unsigned int __dr5;
 unsigned int __dr6;
 unsigned int __dr7;
};
struct __darwin_x86_thread_state64
{
 __uint64_t __rax;
 __uint64_t __rbx;
 __uint64_t __rcx;
 __uint64_t __rdx;
 __uint64_t __rdi;
 __uint64_t __rsi;
 __uint64_t __rbp;
 __uint64_t __rsp;
 __uint64_t __r8;
 __uint64_t __r9;
 __uint64_t __r10;
 __uint64_t __r11;
 __uint64_t __r12;
 __uint64_t __r13;
 __uint64_t __r14;
 __uint64_t __r15;
 __uint64_t __rip;
 __uint64_t __rflags;
 __uint64_t __cs;
 __uint64_t __fs;
 __uint64_t __gs;
};
struct __darwin_x86_float_state64
{
 int __fpu_reserved[2];
 struct __darwin_fp_control __fpu_fcw;
 struct __darwin_fp_status __fpu_fsw;
 __uint8_t __fpu_ftw;
 __uint8_t __fpu_rsrv1;
 __uint16_t __fpu_fop;
 __uint32_t __fpu_ip;
 __uint16_t __fpu_cs;
 __uint16_t __fpu_rsrv2;
 __uint32_t __fpu_dp;
 __uint16_t __fpu_ds;
 __uint16_t __fpu_rsrv3;
 __uint32_t __fpu_mxcsr;
 __uint32_t __fpu_mxcsrmask;
 struct __darwin_mmst_reg __fpu_stmm0;
 struct __darwin_mmst_reg __fpu_stmm1;
 struct __darwin_mmst_reg __fpu_stmm2;
 struct __darwin_mmst_reg __fpu_stmm3;
 struct __darwin_mmst_reg __fpu_stmm4;
 struct __darwin_mmst_reg __fpu_stmm5;
 struct __darwin_mmst_reg __fpu_stmm6;
 struct __darwin_mmst_reg __fpu_stmm7;
 struct __darwin_xmm_reg __fpu_xmm0;
 struct __darwin_xmm_reg __fpu_xmm1;
 struct __darwin_xmm_reg __fpu_xmm2;
 struct __darwin_xmm_reg __fpu_xmm3;
 struct __darwin_xmm_reg __fpu_xmm4;
 struct __darwin_xmm_reg __fpu_xmm5;
 struct __darwin_xmm_reg __fpu_xmm6;
 struct __darwin_xmm_reg __fpu_xmm7;
 struct __darwin_xmm_reg __fpu_xmm8;
 struct __darwin_xmm_reg __fpu_xmm9;
 struct __darwin_xmm_reg __fpu_xmm10;
 struct __darwin_xmm_reg __fpu_xmm11;
 struct __darwin_xmm_reg __fpu_xmm12;
 struct __darwin_xmm_reg __fpu_xmm13;
 struct __darwin_xmm_reg __fpu_xmm14;
 struct __darwin_xmm_reg __fpu_xmm15;
 char __fpu_rsrv4[6*16];
 int __fpu_reserved1;
};
struct __darwin_x86_avx_state64
{
 int __fpu_reserved[2];
 struct __darwin_fp_control __fpu_fcw;
 struct __darwin_fp_status __fpu_fsw;
 __uint8_t __fpu_ftw;
 __uint8_t __fpu_rsrv1;
 __uint16_t __fpu_fop;
 __uint32_t __fpu_ip;
 __uint16_t __fpu_cs;
 __uint16_t __fpu_rsrv2;
 __uint32_t __fpu_dp;
 __uint16_t __fpu_ds;
 __uint16_t __fpu_rsrv3;
 __uint32_t __fpu_mxcsr;
 __uint32_t __fpu_mxcsrmask;
 struct __darwin_mmst_reg __fpu_stmm0;
 struct __darwin_mmst_reg __fpu_stmm1;
 struct __darwin_mmst_reg __fpu_stmm2;
 struct __darwin_mmst_reg __fpu_stmm3;
 struct __darwin_mmst_reg __fpu_stmm4;
 struct __darwin_mmst_reg __fpu_stmm5;
 struct __darwin_mmst_reg __fpu_stmm6;
 struct __darwin_mmst_reg __fpu_stmm7;
 struct __darwin_xmm_reg __fpu_xmm0;
 struct __darwin_xmm_reg __fpu_xmm1;
 struct __darwin_xmm_reg __fpu_xmm2;
 struct __darwin_xmm_reg __fpu_xmm3;
 struct __darwin_xmm_reg __fpu_xmm4;
 struct __darwin_xmm_reg __fpu_xmm5;
 struct __darwin_xmm_reg __fpu_xmm6;
 struct __darwin_xmm_reg __fpu_xmm7;
 struct __darwin_xmm_reg __fpu_xmm8;
 struct __darwin_xmm_reg __fpu_xmm9;
 struct __darwin_xmm_reg __fpu_xmm10;
 struct __darwin_xmm_reg __fpu_xmm11;
 struct __darwin_xmm_reg __fpu_xmm12;
 struct __darwin_xmm_reg __fpu_xmm13;
 struct __darwin_xmm_reg __fpu_xmm14;
 struct __darwin_xmm_reg __fpu_xmm15;
 char __fpu_rsrv4[6*16];
 int __fpu_reserved1;
 char __avx_reserved1[64];
 struct __darwin_xmm_reg __fpu_ymmh0;
 struct __darwin_xmm_reg __fpu_ymmh1;
 struct __darwin_xmm_reg __fpu_ymmh2;
 struct __darwin_xmm_reg __fpu_ymmh3;
 struct __darwin_xmm_reg __fpu_ymmh4;
 struct __darwin_xmm_reg __fpu_ymmh5;
 struct __darwin_xmm_reg __fpu_ymmh6;
 struct __darwin_xmm_reg __fpu_ymmh7;
 struct __darwin_xmm_reg __fpu_ymmh8;
 struct __darwin_xmm_reg __fpu_ymmh9;
 struct __darwin_xmm_reg __fpu_ymmh10;
 struct __darwin_xmm_reg __fpu_ymmh11;
 struct __darwin_xmm_reg __fpu_ymmh12;
 struct __darwin_xmm_reg __fpu_ymmh13;
 struct __darwin_xmm_reg __fpu_ymmh14;
 struct __darwin_xmm_reg __fpu_ymmh15;
};
struct __darwin_x86_exception_state64
{
    __uint16_t __trapno;
    __uint16_t __cpu;
    __uint32_t __err;
    __uint64_t __faultvaddr;
};
struct __darwin_x86_debug_state64
{
 __uint64_t __dr0;
 __uint64_t __dr1;
 __uint64_t __dr2;
 __uint64_t __dr3;
 __uint64_t __dr4;
 __uint64_t __dr5;
 __uint64_t __dr6;
 __uint64_t __dr7;
};
struct __darwin_mcontext32
{
 struct __darwin_i386_exception_state __es;
 struct __darwin_i386_thread_state __ss;
 struct __darwin_i386_float_state __fs;
};
struct __darwin_mcontext_avx32
{
 struct __darwin_i386_exception_state __es;
 struct __darwin_i386_thread_state __ss;
 struct __darwin_i386_avx_state __fs;
};
struct __darwin_mcontext64
{
 struct __darwin_x86_exception_state64 __es;
 struct __darwin_x86_thread_state64 __ss;
 struct __darwin_x86_float_state64 __fs;
};
struct __darwin_mcontext_avx64
{
 struct __darwin_x86_exception_state64 __es;
 struct __darwin_x86_thread_state64 __ss;
 struct __darwin_x86_avx_state64 __fs;
};
typedef struct __darwin_mcontext64 *mcontext_t;
typedef __darwin_pthread_attr_t pthread_attr_t;
struct __darwin_sigaltstack
{
 void *ss_sp;
 __darwin_size_t ss_size;
 int ss_flags;
};
typedef struct __darwin_sigaltstack stack_t;
struct __darwin_ucontext
{
 int uc_onstack;
 __darwin_sigset_t uc_sigmask;
 struct __darwin_sigaltstack uc_stack;
 struct __darwin_ucontext *uc_link;
 __darwin_size_t uc_mcsize;
 struct __darwin_mcontext64 *uc_mcontext;
};
typedef struct __darwin_ucontext ucontext_t;
typedef __darwin_pid_t pid_t;
typedef __darwin_sigset_t sigset_t;
typedef __darwin_size_t size_t;
typedef __darwin_uid_t uid_t;
union sigval {
 int sival_int;
 void *sival_ptr;
};
struct sigevent {
 int sigev_notify;
 int sigev_signo;
 union sigval sigev_value;
 void (*sigev_notify_function)(union sigval);
 pthread_attr_t *sigev_notify_attributes;
};
typedef struct __siginfo {
 int si_signo;
 int si_errno;
 int si_code;
 pid_t si_pid;
 uid_t si_uid;
 int si_status;
 void *si_addr;
 union sigval si_value;
 long si_band;
 unsigned long __pad[7];
} siginfo_t;
union __sigaction_u {
 void (*__sa_handler)(int);
 void (*__sa_sigaction)(int, struct __siginfo *,
         void *);
};
struct __sigaction {
 union __sigaction_u __sigaction_u;
 void (*sa_tramp)(void *, int, int, siginfo_t *, void *);
 sigset_t sa_mask;
 int sa_flags;
};
struct sigaction {
 union __sigaction_u __sigaction_u;
 sigset_t sa_mask;
 int sa_flags;
};
typedef void (*sig_t)(int);
struct sigvec {
 void (*sv_handler)(int);
 int sv_mask;
 int sv_flags;
};
struct sigstack {
 char *ss_sp;
 int ss_onstack;
};
void (*signal(int, void (*)(int)))(int);
struct timespec
{
 __darwin_time_t tv_sec;
 long tv_nsec;
};
typedef __darwin_off_t off_t;
typedef __darwin_ssize_t ssize_t;
struct aiocb {
 int aio_fildes;
 off_t aio_offset;
 volatile void *aio_buf;
 size_t aio_nbytes;
 int aio_reqprio;
 struct sigevent aio_sigevent;
 int aio_lio_opcode;
};
int aio_cancel( int fd,
     struct aiocb * aiocbp );
int aio_error( const struct aiocb * aiocbp );
int aio_fsync( int op,
       struct aiocb * aiocbp );
int aio_read( struct aiocb * aiocbp );
ssize_t aio_return( struct aiocb * aiocbp );
int aio_suspend( const struct aiocb *const aiocblist[],
      int nent,
       const struct timespec * timeoutp );
int aio_write( struct aiocb * aiocbp );
int lio_listio( int mode,
     struct aiocb *const aiocblist[],
      int nent,
      struct sigevent *sigp );
char *basename(char *);
char *dirname(char *);
typedef int __darwin_nl_item;
typedef int __darwin_wctrans_t;
typedef __uint32_t __darwin_wctype_t;
typedef __darwin_mode_t mode_t;
typedef void *posix_spawnattr_t;
typedef void *posix_spawn_file_actions_t;
int posix_spawn(pid_t * restrict, const char * restrict,
  const posix_spawn_file_actions_t *,
  const posix_spawnattr_t * restrict,
  char *const __argv[],
  char *const __envp[]) ;
int posix_spawnp(pid_t * restrict, const char * restrict,
  const posix_spawn_file_actions_t *,
  const posix_spawnattr_t * restrict,
  char *const __argv[],
  char *const __envp[]) ;
int posix_spawn_file_actions_addclose(posix_spawn_file_actions_t *, int) ;
int posix_spawn_file_actions_adddup2(posix_spawn_file_actions_t *, int,
  int) ;
int posix_spawn_file_actions_addopen(
  posix_spawn_file_actions_t * restrict, int,
  const char * restrict, int, mode_t) ;
int posix_spawn_file_actions_destroy(posix_spawn_file_actions_t *) ;
int posix_spawn_file_actions_init(posix_spawn_file_actions_t *) ;
int posix_spawnattr_destroy(posix_spawnattr_t *) ;
int posix_spawnattr_getsigdefault(const posix_spawnattr_t * restrict,
  sigset_t * restrict) ;
int posix_spawnattr_getflags(const posix_spawnattr_t * restrict,
  short * restrict) ;
int posix_spawnattr_getpgroup(const posix_spawnattr_t * restrict,
  pid_t * restrict) ;
int posix_spawnattr_getsigmask(const posix_spawnattr_t * restrict,
  sigset_t * restrict) ;
int posix_spawnattr_init(posix_spawnattr_t *) ;
int posix_spawnattr_setsigdefault(posix_spawnattr_t * restrict,
  const sigset_t * restrict) ;
int posix_spawnattr_setflags(posix_spawnattr_t *, short) ;
int posix_spawnattr_setpgroup(posix_spawnattr_t *, pid_t) ;
int posix_spawnattr_setsigmask(posix_spawnattr_t * restrict,
  const sigset_t * restrict) ;
typedef signed char int8_t;
typedef short int16_t;
typedef int int32_t;
typedef long long int64_t;
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
typedef __darwin_intptr_t intptr_t;
typedef unsigned long uintptr_t;
typedef long int intmax_t;
typedef long unsigned int uintmax_t;
typedef unsigned int boolean_t;
typedef __darwin_natural_t natural_t;
typedef int integer_t;
typedef uintptr_t vm_offset_t;
typedef uintptr_t vm_size_t;
typedef uint64_t mach_vm_address_t;
typedef uint64_t mach_vm_offset_t;
typedef uint64_t mach_vm_size_t;
typedef uint64_t vm_map_offset_t;
typedef uint64_t vm_map_address_t;
typedef uint64_t vm_map_size_t;
typedef mach_vm_address_t mach_port_context_t;
typedef natural_t mach_port_name_t;
typedef mach_port_name_t *mach_port_name_array_t;
typedef __darwin_mach_port_t mach_port_t;
typedef mach_port_t *mach_port_array_t;
typedef natural_t mach_port_right_t;
typedef natural_t mach_port_type_t;
typedef mach_port_type_t *mach_port_type_array_t;
typedef natural_t mach_port_urefs_t;
typedef integer_t mach_port_delta_t;
typedef natural_t mach_port_seqno_t;
typedef natural_t mach_port_mscount_t;
typedef natural_t mach_port_msgcount_t;
typedef natural_t mach_port_rights_t;
typedef unsigned int mach_port_srights_t;
typedef struct mach_port_status {
 mach_port_rights_t mps_pset;
 mach_port_seqno_t mps_seqno;
 mach_port_mscount_t mps_mscount;
 mach_port_msgcount_t mps_qlimit;
 mach_port_msgcount_t mps_msgcount;
 mach_port_rights_t mps_sorights;
 boolean_t mps_srights;
 boolean_t mps_pdrequest;
 boolean_t mps_nsrequest;
 natural_t mps_flags;
} mach_port_status_t;
typedef struct mach_port_limits {
 mach_port_msgcount_t mpl_qlimit;
} mach_port_limits_t;
typedef struct mach_port_info_ext {
 mach_port_status_t mpie_status;
 mach_port_msgcount_t mpie_boost_cnt;
 uint32_t reserved[6];
} mach_port_info_ext_t;
typedef integer_t *mach_port_info_t;
typedef int mach_port_flavor_t;
typedef struct mach_port_qos {
 unsigned int name:1;
 unsigned int prealloc:1;
 boolean_t pad1:30;
 natural_t len;
} mach_port_qos_t;
typedef struct mach_port_options {
 uint32_t flags;
 mach_port_limits_t mpl;
 uint64_t reserved[2];
}mach_port_options_t;
typedef mach_port_options_t *mach_port_options_ptr_t;
enum mach_port_guard_exception_codes {
 kGUARD_EXC_DESTROY = 1u << 0,
 kGUARD_EXC_MOD_REFS = 1u << 1,
 kGUARD_EXC_SET_CONTEXT = 1u << 2,
 kGUARD_EXC_UNGUARDED = 1u << 3,
 kGUARD_EXC_INCORRECT_GUARD = 1u << 4
};
typedef int kern_return_t;
typedef natural_t mach_msg_timeout_t;
typedef unsigned int mach_msg_bits_t;
typedef natural_t mach_msg_size_t;
typedef integer_t mach_msg_id_t;
typedef unsigned int mach_msg_type_name_t;
typedef unsigned int mach_msg_copy_options_t;
typedef unsigned int mach_msg_descriptor_type_t;
typedef struct
{
  natural_t pad1;
  mach_msg_size_t pad2;
  unsigned int pad3 : 24;
  mach_msg_descriptor_type_t type : 8;
} mach_msg_type_descriptor_t;
typedef struct
{
  mach_port_t name;
  mach_msg_size_t pad1;
  unsigned int pad2 : 16;
  mach_msg_type_name_t disposition : 8;
  mach_msg_descriptor_type_t type : 8;
} mach_msg_port_descriptor_t;
typedef struct
{
  uint32_t address;
  mach_msg_size_t size;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  unsigned int pad1: 8;
  mach_msg_descriptor_type_t type: 8;
} mach_msg_ool_descriptor32_t;
typedef struct
{
  uint64_t address;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  unsigned int pad1: 8;
  mach_msg_descriptor_type_t type: 8;
  mach_msg_size_t size;
} mach_msg_ool_descriptor64_t;
typedef struct
{
  void* address;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  unsigned int pad1: 8;
  mach_msg_descriptor_type_t type: 8;
  mach_msg_size_t size;
} mach_msg_ool_descriptor_t;
typedef struct
{
  uint32_t address;
  mach_msg_size_t count;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  mach_msg_type_name_t disposition : 8;
  mach_msg_descriptor_type_t type : 8;
} mach_msg_ool_ports_descriptor32_t;
typedef struct
{
  uint64_t address;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  mach_msg_type_name_t disposition : 8;
  mach_msg_descriptor_type_t type : 8;
  mach_msg_size_t count;
} mach_msg_ool_ports_descriptor64_t;
typedef struct
{
  void* address;
  boolean_t deallocate: 8;
  mach_msg_copy_options_t copy: 8;
  mach_msg_type_name_t disposition : 8;
  mach_msg_descriptor_type_t type : 8;
  mach_msg_size_t count;
} mach_msg_ool_ports_descriptor_t;
typedef union
{
  mach_msg_port_descriptor_t port;
  mach_msg_ool_descriptor_t out_of_line;
  mach_msg_ool_ports_descriptor_t ool_ports;
  mach_msg_type_descriptor_t type;
} mach_msg_descriptor_t;
typedef struct
{
        mach_msg_size_t msgh_descriptor_count;
} mach_msg_body_t;
typedef struct
{
  mach_msg_bits_t msgh_bits;
  mach_msg_size_t msgh_size;
  mach_port_t msgh_remote_port;
  mach_port_t msgh_local_port;
  mach_port_name_t msgh_voucher_port;
  mach_msg_id_t msgh_id;
} mach_msg_header_t;
typedef struct
{
        mach_msg_header_t header;
        mach_msg_body_t body;
} mach_msg_base_t;
typedef unsigned int mach_msg_trailer_type_t;
typedef unsigned int mach_msg_trailer_size_t;
typedef char *mach_msg_trailer_info_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
} mach_msg_trailer_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
  mach_port_seqno_t msgh_seqno;
} mach_msg_seqno_trailer_t;
typedef struct
{
  unsigned int val[2];
} security_token_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
  mach_port_seqno_t msgh_seqno;
  security_token_t msgh_sender;
} mach_msg_security_trailer_t;
typedef struct
{
  unsigned int val[8];
} audit_token_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
  mach_port_seqno_t msgh_seqno;
  security_token_t msgh_sender;
  audit_token_t msgh_audit;
} mach_msg_audit_trailer_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
  mach_port_seqno_t msgh_seqno;
  security_token_t msgh_sender;
  audit_token_t msgh_audit;
  mach_port_context_t msgh_context;
} mach_msg_context_trailer_t;
typedef struct
{
  mach_port_name_t sender;
} msg_labels_t;
typedef struct
{
  mach_msg_trailer_type_t msgh_trailer_type;
  mach_msg_trailer_size_t msgh_trailer_size;
  mach_port_seqno_t msgh_seqno;
  security_token_t msgh_sender;
  audit_token_t msgh_audit;
  mach_port_context_t msgh_context;
  int msgh_ad;
  msg_labels_t msgh_labels;
} mach_msg_mac_trailer_t;
typedef mach_msg_mac_trailer_t mach_msg_max_trailer_t;
typedef mach_msg_security_trailer_t mach_msg_format_0_trailer_t;
extern security_token_t KERNEL_SECURITY_TOKEN;
extern audit_token_t KERNEL_AUDIT_TOKEN;
typedef integer_t mach_msg_options_t;
typedef struct
{
  mach_msg_header_t header;
} mach_msg_empty_send_t;
typedef struct
{
  mach_msg_header_t header;
  mach_msg_trailer_t trailer;
} mach_msg_empty_rcv_t;
typedef union
{
  mach_msg_empty_send_t send;
  mach_msg_empty_rcv_t rcv;
} mach_msg_empty_t;
typedef natural_t mach_msg_type_size_t;
typedef natural_t mach_msg_type_number_t;
typedef integer_t mach_msg_option_t;
typedef kern_return_t mach_msg_return_t;
extern mach_msg_return_t mach_msg_overwrite(
     mach_msg_header_t *msg,
     mach_msg_option_t option,
     mach_msg_size_t send_size,
     mach_msg_size_t rcv_size,
     mach_port_name_t rcv_name,
     mach_msg_timeout_t timeout,
     mach_port_name_t notify,
     mach_msg_header_t *rcv_msg,
     mach_msg_size_t rcv_limit);
extern mach_msg_return_t mach_msg(
     mach_msg_header_t *msg,
     mach_msg_option_t option,
     mach_msg_size_t send_size,
     mach_msg_size_t rcv_size,
     mach_port_name_t rcv_name,
     mach_msg_timeout_t timeout,
     mach_port_name_t notify);
extern kern_return_t mach_voucher_deallocate(
     mach_port_name_t voucher);
struct x86_state_hdr {
 int flavor;
 int count;
};
typedef struct x86_state_hdr x86_state_hdr_t;
typedef struct __darwin_i386_thread_state i386_thread_state_t;
typedef struct __darwin_i386_thread_state x86_thread_state32_t;
typedef struct __darwin_i386_float_state i386_float_state_t;
typedef struct __darwin_i386_float_state x86_float_state32_t;
typedef struct __darwin_i386_avx_state x86_avx_state32_t;
typedef struct __darwin_i386_exception_state i386_exception_state_t;
typedef struct __darwin_i386_exception_state x86_exception_state32_t;
typedef struct __darwin_x86_debug_state32 x86_debug_state32_t;
typedef struct __darwin_x86_thread_state64 x86_thread_state64_t;
typedef struct __darwin_x86_float_state64 x86_float_state64_t;
typedef struct __darwin_x86_avx_state64 x86_avx_state64_t;
typedef struct __darwin_x86_exception_state64 x86_exception_state64_t;
typedef struct __darwin_x86_debug_state64 x86_debug_state64_t;
struct x86_thread_state {
 x86_state_hdr_t tsh;
 union {
     x86_thread_state32_t ts32;
     x86_thread_state64_t ts64;
 } uts;
};
struct x86_float_state {
 x86_state_hdr_t fsh;
 union {
  x86_float_state32_t fs32;
  x86_float_state64_t fs64;
 } ufs;
};
struct x86_exception_state {
 x86_state_hdr_t esh;
 union {
  x86_exception_state32_t es32;
  x86_exception_state64_t es64;
 } ues;
};
struct x86_debug_state {
 x86_state_hdr_t dsh;
 union {
  x86_debug_state32_t ds32;
  x86_debug_state64_t ds64;
 } uds;
};
struct x86_avx_state {
 x86_state_hdr_t ash;
 union {
  x86_avx_state32_t as32;
  x86_avx_state64_t as64;
 } ufs;
};
typedef struct x86_thread_state x86_thread_state_t;
typedef struct x86_float_state x86_float_state_t;
typedef struct x86_exception_state x86_exception_state_t;
typedef struct x86_debug_state x86_debug_state_t;
typedef struct x86_avx_state x86_avx_state_t;
typedef natural_t *thread_state_t;
typedef natural_t thread_state_data_t[(224)];
typedef int thread_state_flavor_t;
typedef thread_state_flavor_t *thread_state_flavor_array_t;
typedef int exception_type_t;
typedef integer_t exception_data_type_t;
typedef int64_t mach_exception_data_type_t;
typedef int exception_behavior_t;
typedef exception_data_type_t *exception_data_t;
typedef mach_exception_data_type_t *mach_exception_data_t;
typedef unsigned int exception_mask_t;
typedef exception_mask_t *exception_mask_array_t;
typedef exception_behavior_t *exception_behavior_array_t;
typedef thread_state_flavor_t *exception_flavor_array_t;
typedef mach_port_t *exception_port_array_t;
typedef mach_exception_data_type_t mach_exception_code_t;
typedef mach_exception_data_type_t mach_exception_subcode_t;
typedef integer_t cpu_type_t;
typedef integer_t cpu_subtype_t;
typedef integer_t cpu_threadtype_t;
int posix_spawnattr_getbinpref_np(const posix_spawnattr_t * restrict,
  size_t, cpu_type_t *restrict, size_t *restrict) ;
int posix_spawnattr_setauditsessionport_np(posix_spawnattr_t *restrict,
  mach_port_t) ;
int posix_spawnattr_setbinpref_np(posix_spawnattr_t * restrict,
  size_t, cpu_type_t *restrict, size_t *restrict) ;
int posix_spawnattr_setexceptionports_np(posix_spawnattr_t *restrict,
  exception_mask_t, mach_port_t,
  exception_behavior_t, thread_state_flavor_t) ;
int posix_spawnattr_setspecialport_np(posix_spawnattr_t *restrict,
  mach_port_t, int) ;
int posix_spawn_file_actions_addinherit_np(posix_spawn_file_actions_t *,
  int) ;
typedef struct fd_set {
 __int32_t fds_bits[((((1024) % ((sizeof(__int32_t) * 8))) == 0) ? ((1024) / ((sizeof(__int32_t) * 8))) : (((1024) / ((sizeof(__int32_t) * 8))) + 1))];
} fd_set;
int __darwin_fd_isset(int _n, const struct fd_set *_p);
struct timeval
{
 __darwin_time_t tv_sec;
 __darwin_suseconds_t tv_usec;
};
typedef __darwin_time_t time_t;
typedef __darwin_suseconds_t suseconds_t;
struct itimerval {
 struct timeval it_interval;
 struct timeval it_value;
};
struct timezone {
 int tz_minuteswest;
 int tz_dsttime;
};
struct clockinfo {
 int hz;
 int tick;
 int tickadj;
 int stathz;
 int profhz;
};
typedef __darwin_clock_t clock_t;
struct tm {
 int tm_sec;
 int tm_min;
 int tm_hour;
 int tm_mday;
 int tm_mon;
 int tm_year;
 int tm_wday;
 int tm_yday;
 int tm_isdst;
 long tm_gmtoff;
 char *tm_zone;
};
extern char *tzname[];
extern int getdate_err;
extern long timezone;
extern int daylight;
char *asctime(const struct tm *);
clock_t clock(void);
char *ctime(const time_t *);
double difftime(time_t, time_t);
struct tm *getdate(const char *);
struct tm *gmtime(const time_t *);
struct tm *localtime(const time_t *);
time_t mktime(struct tm *);
size_t strftime(char * restrict, size_t, const char * restrict, const struct tm * restrict);
char *strptime(const char * restrict, const char * restrict, struct tm * restrict);
time_t time(time_t *);
void tzset(void);
char *asctime_r(const struct tm * restrict, char * restrict);
char *ctime_r(const time_t *, char *);
struct tm *gmtime_r(const time_t * restrict, struct tm * restrict);
struct tm *localtime_r(const time_t * restrict, struct tm * restrict);
time_t posix2time(time_t);
void tzsetwall(void);
time_t time2posix(time_t);
time_t timelocal(struct tm * const);
time_t timegm(struct tm * const);
int nanosleep(const struct timespec *, struct timespec *);
int adjtime(const struct timeval *, struct timeval *);
int futimes(int, const struct timeval *);
int lutimes(const char *, const struct timeval *) ;
int settimeofday(const struct timeval *, const struct timezone *);
int getitimer(int, struct itimerval *);
int gettimeofday(struct timeval * restrict, void * restrict);
int select(int, fd_set * restrict, fd_set * restrict,
  fd_set * restrict, struct timeval * restrict);

  ;
int setitimer(int, const struct itimerval * restrict,
  struct itimerval * restrict);
int utimes(const char *, const struct timeval *);
static inline
__uint16_t
_OSSwapInt16(
    __uint16_t _data
);
static inline
__uint32_t
_OSSwapInt32(
    __uint32_t _data
);
static inline
__uint64_t
_OSSwapInt64(
    __uint64_t _data
);
typedef __uint32_t in_addr_t;
typedef __uint16_t in_port_t;
typedef unsigned char u_int8_t;
typedef unsigned short u_int16_t;
typedef unsigned int u_int32_t;
typedef unsigned long long u_int64_t;
typedef int64_t register_t;
typedef u_int64_t user_addr_t;
typedef u_int64_t user_size_t;
typedef int64_t user_ssize_t;
typedef int64_t user_long_t;
typedef u_int64_t user_ulong_t;
typedef int64_t user_time_t;
typedef int64_t user_off_t;
typedef u_int64_t syscall_arg_t;
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
typedef __darwin_ino_t ino_t;
typedef __darwin_ino64_t ino64_t;
typedef __int32_t key_t;
typedef __uint16_t nlink_t;
typedef __darwin_id_t id_t;
typedef int32_t segsz_t;
typedef int32_t swblk_t;
typedef __darwin_useconds_t useconds_t;
typedef __darwin_size_t rsize_t;
typedef int errno_t;
typedef __int32_t fd_mask;
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
typedef __uint8_t sa_family_t;
typedef __darwin_socklen_t socklen_t;
struct iovec {
 void * iov_base;
 size_t iov_len;
};
struct linger {
 int l_onoff;
 int l_linger;
};
struct so_np_extensions {
 u_int32_t npx_flags;
 u_int32_t npx_mask;
};
struct sockaddr {
 __uint8_t sa_len;
 sa_family_t sa_family;
 char sa_data[14];
};
struct sockproto {
 __uint16_t sp_family;
 __uint16_t sp_protocol;
};
struct sockaddr_storage {
 __uint8_t ss_len;
 sa_family_t ss_family;
 char __ss_pad1[((sizeof(__int64_t)) - sizeof(__uint8_t) - sizeof(sa_family_t))];
 __int64_t __ss_align;
 char __ss_pad2[(128 - sizeof(__uint8_t) - sizeof(sa_family_t) - ((sizeof(__int64_t)) - sizeof(__uint8_t) - sizeof(sa_family_t)) - (sizeof(__int64_t)))];
};
struct msghdr {
 void *msg_name;
 socklen_t msg_namelen;
 struct iovec *msg_iov;
 int msg_iovlen;
 void *msg_control;
 socklen_t msg_controllen;
 int msg_flags;
};
struct cmsghdr {
 socklen_t cmsg_len;
 int cmsg_level;
 int cmsg_type;
};
struct sf_hdtr {
 struct iovec *headers;
 int hdr_cnt;
 struct iovec *trailers;
 int trl_cnt;
};
int accept(int, struct sockaddr * restrict, socklen_t * restrict);

int bind(int, const struct sockaddr *, socklen_t);
int connect(int, const struct sockaddr *, socklen_t);
int getpeername(int, struct sockaddr * restrict, socklen_t * restrict);

int getsockname(int, struct sockaddr * restrict, socklen_t * restrict);

int getsockopt(int, int, int, void * restrict, socklen_t * restrict);
int listen(int, int);
ssize_t recv(int, void *, size_t, int);
ssize_t recvfrom(int, void *, size_t, int, struct sockaddr * restrict,
  socklen_t * restrict);
ssize_t recvmsg(int, struct msghdr *, int);
ssize_t send(int, const void *, size_t, int);
ssize_t sendmsg(int, const struct msghdr *, int);
ssize_t sendto(int, const void *, size_t,
  int, const struct sockaddr *, socklen_t);
int setsockopt(int, int, int, const void *, socklen_t);
int shutdown(int, int);
int sockatmark(int) ;
int socket(int, int, int);
int socketpair(int, int, int, int *);
int sendfile(int, int, off_t, off_t *, struct sf_hdtr *, int);
void pfctlinput(int, struct sockaddr *);
struct in_addr {
 in_addr_t s_addr;
};
struct sockaddr_in {
 __uint8_t sin_len;
 sa_family_t sin_family;
 in_port_t sin_port;
 struct in_addr sin_addr;
 char sin_zero[8];
};
struct ip_opts {
 struct in_addr ip_dst;
 char ip_opts[40];
};
struct ip_mreq {
 struct in_addr imr_multiaddr;
 struct in_addr imr_interface;
};
struct ip_mreqn {
 struct in_addr imr_multiaddr;
 struct in_addr imr_address;
 int imr_ifindex;
};
struct ip_mreq_source {
 struct in_addr imr_multiaddr;
 struct in_addr imr_sourceaddr;
 struct in_addr imr_interface;
};
struct group_req {
 uint32_t gr_interface;
 struct sockaddr_storage gr_group;
};
struct group_source_req {
 uint32_t gsr_interface;
 struct sockaddr_storage gsr_group;
 struct sockaddr_storage gsr_source;
};
struct __msfilterreq {
 uint32_t msfr_ifindex;
 uint32_t msfr_fmode;
 uint32_t msfr_nsrcs;
 uint32_t __msfr_align;
 struct sockaddr_storage msfr_group;
 struct sockaddr_storage *msfr_srcs;
};
struct sockaddr;
int setipv4sourcefilter(int, struct in_addr, struct in_addr, uint32_t,
     uint32_t, struct in_addr *) ;
int getipv4sourcefilter(int, struct in_addr, struct in_addr, uint32_t *,
     uint32_t *, struct in_addr *) ;
int setsourcefilter(int, uint32_t, struct sockaddr *, socklen_t,
     uint32_t, uint32_t, struct sockaddr_storage *) ;
int getsourcefilter(int, uint32_t, struct sockaddr *, socklen_t,
     uint32_t *, uint32_t *, struct sockaddr_storage *) ;
struct in_pktinfo {
 unsigned int ipi_ifindex;
 struct in_addr ipi_spec_dst;
 struct in_addr ipi_addr;
};
struct in6_addr {
 union {
  __uint8_t __u6_addr8[16];
  __uint16_t __u6_addr16[8];
  __uint32_t __u6_addr32[4];
 } __u6_addr;
};
struct sockaddr_in6 {
 __uint8_t sin6_len;
 sa_family_t sin6_family;
 in_port_t sin6_port;
 __uint32_t sin6_flowinfo;
 struct in6_addr sin6_addr;
 __uint32_t sin6_scope_id;
};
extern const struct in6_addr in6addr_any;
extern const struct in6_addr in6addr_loopback;
extern const struct in6_addr in6addr_nodelocal_allnodes;
extern const struct in6_addr in6addr_linklocal_allnodes;
extern const struct in6_addr in6addr_linklocal_allrouters;
extern const struct in6_addr in6addr_linklocal_allv2routers;
struct ipv6_mreq {
 struct in6_addr ipv6mr_multiaddr;
 unsigned int ipv6mr_interface;
};
struct in6_pktinfo {
 struct in6_addr ipi6_addr;
 unsigned int ipi6_ifindex;
};
struct ip6_mtuinfo {
 struct sockaddr_in6 ip6m_addr;
 uint32_t ip6m_mtu;
};
struct cmsghdr;
extern int inet6_option_space(int);
extern int inet6_option_init(void *, struct cmsghdr **, int);
extern int inet6_option_append(struct cmsghdr *, const __uint8_t *, int, int);
extern __uint8_t *inet6_option_alloc(struct cmsghdr *, int, int, int);
extern int inet6_option_next(const struct cmsghdr *, __uint8_t **);
extern int inet6_option_find(const struct cmsghdr *, __uint8_t **, int);
extern size_t inet6_rthdr_space(int, int);
extern struct cmsghdr *inet6_rthdr_init(void *, int);
extern int inet6_rthdr_add(struct cmsghdr *, const struct in6_addr *,
    unsigned int);
extern int inet6_rthdr_lasthop(struct cmsghdr *, unsigned int);
extern int inet6_rthdr_segments(const struct cmsghdr *);
extern struct in6_addr *inet6_rthdr_getaddr(struct cmsghdr *, int);
extern int inet6_rthdr_getflags(const struct cmsghdr *, int);
extern int inet6_opt_init(void *, socklen_t);
extern int inet6_opt_append(void *, socklen_t, int, __uint8_t, socklen_t,
    __uint8_t, void **);
extern int inet6_opt_finish(void *, socklen_t, int);
extern int inet6_opt_set_val(void *, int, void *, socklen_t);
extern int inet6_opt_next(void *, socklen_t, int, __uint8_t *, socklen_t *,
    void **);
extern int inet6_opt_find(void *, socklen_t, int, __uint8_t, socklen_t *,
    void **);
extern int inet6_opt_get_val(void *, int, void *, socklen_t);
extern socklen_t inet6_rth_space(int, int);
extern void *inet6_rth_init(void *, socklen_t, int, int);
extern int inet6_rth_add(void *, const struct in6_addr *);
extern int inet6_rth_reverse(const void *, void *);
extern int inet6_rth_segments(const void *);
extern struct in6_addr *inet6_rth_getaddr(const void *, int);
extern void addrsel_policy_init(void);
int bindresvport(int, struct sockaddr_in *);
struct sockaddr;
int bindresvport_sa(int, struct sockaddr *);
in_addr_t inet_addr(const char *);
char *inet_ntoa(struct in_addr);
const char *inet_ntop(int, const void *, char *, socklen_t);
int inet_pton(int, const char *, void *);
int ascii2addr(int, const char *, void *);
char *addr2ascii(int, const void *, int, char *);
int inet_aton(const char *, struct in_addr *);
in_addr_t inet_lnaof(struct in_addr);
struct in_addr inet_makeaddr(in_addr_t, in_addr_t);
in_addr_t inet_netof(struct in_addr);
in_addr_t inet_network(const char *);
char *inet_net_ntop(int, const void *, int, char *, __darwin_size_t);
int inet_net_pton(int, const char *, void *, __darwin_size_t);
char *inet_neta(in_addr_t, char *, __darwin_size_t);
unsigned int inet_nsap_addr(const char *, unsigned char *, int);
char *inet_nsap_ntoa(int, const unsigned char *, char *);
typedef __builtin_va_list va_list;
typedef __builtin_va_list __gnuc_va_list;
struct tms {
 clock_t tms_utime;
 clock_t tms_stime;
 clock_t tms_cutime;
 clock_t tms_cstime;
};
clock_t times(struct tms *);
void __assert_rtn(const char *, const char *, int, const char *) ;
struct lconv {
 char *decimal_point;
 char *thousands_sep;
 char *grouping;
 char *int_curr_symbol;
 char *currency_symbol;
 char *mon_decimal_point;
 char *mon_thousands_sep;
 char *mon_grouping;
 char *positive_sign;
 char *negative_sign;
 char int_frac_digits;
 char frac_digits;
 char p_cs_precedes;
 char p_sep_by_space;
 char n_cs_precedes;
 char n_sep_by_space;
 char p_sign_posn;
 char n_sign_posn;
 char int_p_cs_precedes;
 char int_n_cs_precedes;
 char int_p_sep_by_space;
 char int_n_sep_by_space;
 char int_p_sign_posn;
 char int_n_sign_posn;
};
struct lconv *localeconv(void);
char *setlocale(int, const char *);
extern float _Complex cacosf(float _Complex);
extern double _Complex cacos(double _Complex);
extern long double _Complex cacosl(long double _Complex);
extern float _Complex casinf(float _Complex);
extern double _Complex casin(double _Complex);
extern long double _Complex casinl(long double _Complex);
extern float _Complex catanf(float _Complex);
extern double _Complex catan(double _Complex);
extern long double _Complex catanl(long double _Complex);
extern float _Complex ccosf(float _Complex);
extern double _Complex ccos(double _Complex);
extern long double _Complex ccosl(long double _Complex);
extern float _Complex csinf(float _Complex);
extern double _Complex csin(double _Complex);
extern long double _Complex csinl(long double _Complex);
extern float _Complex ctanf(float _Complex);
extern double _Complex ctan(double _Complex);
extern long double _Complex ctanl(long double _Complex);
extern float _Complex cacoshf(float _Complex);
extern double _Complex cacosh(double _Complex);
extern long double _Complex cacoshl(long double _Complex);
extern float _Complex casinhf(float _Complex);
extern double _Complex casinh(double _Complex);
extern long double _Complex casinhl(long double _Complex);
extern float _Complex catanhf(float _Complex);
extern double _Complex catanh(double _Complex);
extern long double _Complex catanhl(long double _Complex);
extern float _Complex ccoshf(float _Complex);
extern double _Complex ccosh(double _Complex);
extern long double _Complex ccoshl(long double _Complex);
extern float _Complex csinhf(float _Complex);
extern double _Complex csinh(double _Complex);
extern long double _Complex csinhl(long double _Complex);
extern float _Complex ctanhf(float _Complex);
extern double _Complex ctanh(double _Complex);
extern long double _Complex ctanhl(long double _Complex);
extern float _Complex cexpf(float _Complex);
extern double _Complex cexp(double _Complex);
extern long double _Complex cexpl(long double _Complex);
extern float _Complex clogf(float _Complex);
extern double _Complex clog(double _Complex);
extern long double _Complex clogl(long double _Complex);
extern float cabsf(float _Complex);
extern double cabs(double _Complex);
extern long double cabsl(long double _Complex);
extern float _Complex cpowf(float _Complex, float _Complex);
extern double _Complex cpow(double _Complex, double _Complex);
extern long double _Complex cpowl(long double _Complex, long double _Complex);
extern float _Complex csqrtf(float _Complex);
extern double _Complex csqrt(double _Complex);
extern long double _Complex csqrtl(long double _Complex);
extern float cargf(float _Complex);
extern double carg(double _Complex);
extern long double cargl(long double _Complex);
extern float cimagf(float _Complex);
extern double cimag(double _Complex);
extern long double cimagl(long double _Complex);
extern float _Complex conjf(float _Complex);
extern double _Complex conj(double _Complex);
extern long double _Complex conjl(long double _Complex);
extern float _Complex cprojf(float _Complex);
extern double _Complex cproj(double _Complex);
extern long double _Complex cprojl(long double _Complex);
extern float crealf(float _Complex);
extern double creal(double _Complex);
extern long double creall(long double _Complex);
    typedef float float_t;
    typedef double double_t;
extern int __math_errhandling(void);
extern int __fpclassifyf(float);
extern int __fpclassifyd(double);
extern int __fpclassifyl(long double);
extern float acosf(float);
extern double acos(double);
extern long double acosl(long double);
extern float asinf(float);
extern double asin(double);
extern long double asinl(long double);
extern float atanf(float);
extern double atan(double);
extern long double atanl(long double);
extern float atan2f(float, float);
extern double atan2(double, double);
extern long double atan2l(long double, long double);
extern float cosf(float);
extern double cos(double);
extern long double cosl(long double);
extern float sinf(float);
extern double sin(double);
extern long double sinl(long double);
extern float tanf(float);
extern double tan(double);
extern long double tanl(long double);
extern float acoshf(float);
extern double acosh(double);
extern long double acoshl(long double);
extern float asinhf(float);
extern double asinh(double);
extern long double asinhl(long double);
extern float atanhf(float);
extern double atanh(double);
extern long double atanhl(long double);
extern float coshf(float);
extern double cosh(double);
extern long double coshl(long double);
extern float sinhf(float);
extern double sinh(double);
extern long double sinhl(long double);
extern float tanhf(float);
extern double tanh(double);
extern long double tanhl(long double);
extern float expf(float);
extern double exp(double);
extern long double expl(long double);
extern float exp2f(float);
extern double exp2(double);
extern long double exp2l(long double);
extern float expm1f(float);
extern double expm1(double);
extern long double expm1l(long double);
extern float logf(float);
extern double log(double);
extern long double logl(long double);
extern float log10f(float);
extern double log10(double);
extern long double log10l(long double);
extern float log2f(float);
extern double log2(double);
extern long double log2l(long double);
extern float log1pf(float);
extern double log1p(double);
extern long double log1pl(long double);
extern float logbf(float);
extern double logb(double);
extern long double logbl(long double);
extern float modff(float, float *);
extern double modf(double, double *);
extern long double modfl(long double, long double *);
extern float ldexpf(float, int);
extern double ldexp(double, int);
extern long double ldexpl(long double, int);
extern float frexpf(float, int *);
extern double frexp(double, int *);
extern long double frexpl(long double, int *);
extern int ilogbf(float);
extern int ilogb(double);
extern int ilogbl(long double);
extern float scalbnf(float, int);
extern double scalbn(double, int);
extern long double scalbnl(long double, int);
extern float scalblnf(float, long int);
extern double scalbln(double, long int);
extern long double scalblnl(long double, long int);
extern float fabsf(float);
extern double fabs(double);
extern long double fabsl(long double);
extern float cbrtf(float);
extern double cbrt(double);
extern long double cbrtl(long double);
extern float hypotf(float, float);
extern double hypot(double, double);
extern long double hypotl(long double, long double);
extern float powf(float, float);
extern double pow(double, double);
extern long double powl(long double, long double);
extern float sqrtf(float);
extern double sqrt(double);
extern long double sqrtl(long double);
extern float erff(float);
extern double erf(double);
extern long double erfl(long double);
extern float erfcf(float);
extern double erfc(double);
extern long double erfcl(long double);
extern float lgammaf(float);
extern double lgamma(double);
extern long double lgammal(long double);
extern float tgammaf(float);
extern double tgamma(double);
extern long double tgammal(long double);
extern float ceilf(float);
extern double ceil(double);
extern long double ceill(long double);
extern float floorf(float);
extern double floor(double);
extern long double floorl(long double);
extern float nearbyintf(float);
extern double nearbyint(double);
extern long double nearbyintl(long double);
extern float rintf(float);
extern double rint(double);
extern long double rintl(long double);
extern long int lrintf(float);
extern long int lrint(double);
extern long int lrintl(long double);
extern float roundf(float);
extern double round(double);
extern long double roundl(long double);
extern long int lroundf(float);
extern long int lround(double);
extern long int lroundl(long double);
extern long long int llrintf(float);
extern long long int llrint(double);
extern long long int llrintl(long double);
extern long long int llroundf(float);
extern long long int llround(double);
extern long long int llroundl(long double);
extern float truncf(float);
extern double trunc(double);
extern long double truncl(long double);
extern float fmodf(float, float);
extern double fmod(double, double);
extern long double fmodl(long double, long double);
extern float remainderf(float, float);
extern double remainder(double, double);
extern long double remainderl(long double, long double);
extern float remquof(float, float, int *);
extern double remquo(double, double, int *);
extern long double remquol(long double, long double, int *);
extern float copysignf(float, float);
extern double copysign(double, double);
extern long double copysignl(long double, long double);
extern float nanf(const char *);
extern double nan(const char *);
extern long double nanl(const char *);
extern float nextafterf(float, float);
extern double nextafter(double, double);
extern long double nextafterl(long double, long double);
extern double nexttoward(double, long double);
extern float nexttowardf(float, long double);
extern long double nexttowardl(long double, long double);
extern float fdimf(float, float);
extern double fdim(double, double);
extern long double fdiml(long double, long double);
extern float fmaxf(float, float);
extern double fmax(double, double);
extern long double fmaxl(long double, long double);
extern float fminf(float, float);
extern double fmin(double, double);
extern long double fminl(long double, long double);
extern float fmaf(float, float, float);
extern double fma(double, double, double);
extern long double fmal(long double, long double, long double);
extern float __inff(void) ;
extern double __inf(void) ;
extern long double __infl(void) ;
extern float __nan(void) ;
extern float __exp10f(float) ;
extern double __exp10(double) ;
extern float __cospif(float) ;
extern double __cospi(double) ;
extern float __sinpif(float) ;
extern double __sinpi(double) ;
extern float __tanpif(float) ;
extern double __tanpi(double) ;
struct __float2 { float __sinval; float __cosval; };
struct __double2 { double __sinval; double __cosval; };
extern struct __float2 __sincosf_stret(float);
extern struct __double2 __sincos_stret(double);
extern struct __float2 __sincospif_stret(float);
extern struct __double2 __sincospi_stret(double);
extern double j0(double) ;
extern double j1(double) ;
extern double jn(int, double) ;
extern double y0(double) ;
extern double y1(double) ;
extern double yn(int, double) ;
extern double scalb(double, double);
extern int signgam;
extern long int rinttol(double) ;
extern long int roundtol(double) ;
extern double drem(double, double) ;
extern int finite(double) ;
extern double gamma(double) ;
extern double significand(double) ;
struct exception {
    int type;
    char *name;
    double arg1;
    double arg2;
    double retval;
};
extern int matherr(struct exception *) ;
typedef long int ptrdiff_t;
typedef int wchar_t;
enum uio_rw { UIO_READ, UIO_WRITE };
ssize_t readv(int, const struct iovec *, int);
ssize_t writev(int, const struct iovec *, int);
ssize_t strfmon(char *, size_t, const char *, ...);
struct sockaddr_un {
 unsigned char sun_len;
 sa_family_t sun_family;
 char sun_path[104];
};
typedef __darwin_ct_rune_t ct_rune_t;
typedef __darwin_rune_t rune_t;
typedef __darwin_wint_t wint_t;
typedef struct {
 __darwin_rune_t __min;
 __darwin_rune_t __max;
 __darwin_rune_t __map;
 __uint32_t *__types;
} _RuneEntry;
typedef struct {
 int __nranges;
 _RuneEntry *__ranges;
} _RuneRange;
typedef struct {
 char __name[14];
 __uint32_t __mask;
} _RuneCharClass;
typedef struct {
 char __magic[8];
 char __encoding[32];
 __darwin_rune_t (*__sgetrune)(const char *, __darwin_size_t, char const **);
 int (*__sputrune)(__darwin_rune_t, char *, __darwin_size_t, char **);
 __darwin_rune_t __invalid_rune;
 __uint32_t __runetype[(1 <<8 )];
 __darwin_rune_t __maplower[(1 <<8 )];
 __darwin_rune_t __mapupper[(1 <<8 )];
 _RuneRange __runetype_ext;
 _RuneRange __maplower_ext;
 _RuneRange __mapupper_ext;
 void *__variable;
 int __variable_len;
 int __ncharclasses;
 _RuneCharClass *__charclasses;
} _RuneLocale;
extern _RuneLocale _DefaultRuneLocale;
extern _RuneLocale *_CurrentRuneLocale;
unsigned long ___runetype(__darwin_ct_rune_t);
__darwin_ct_rune_t ___tolower(__darwin_ct_rune_t);
__darwin_ct_rune_t ___toupper(__darwin_ct_rune_t);
typedef __darwin_va_list va_list;
int renameat(int, const char *, int, const char *) ;
typedef __darwin_off_t fpos_t;
struct __sbuf {
 unsigned char *_base;
 int _size;
};
struct __sFILEX;
typedef struct __sFILE {
 unsigned char *_p;
 int _r;
 int _w;
 short _flags;
 short _file;
 struct __sbuf _bf;
 int _lbfsize;
 void *_cookie;
 int (*_close)(void *);
 int (*_read) (void *, char *, int);
 fpos_t (*_seek) (void *, fpos_t, int);
 int (*_write)(void *, const char *, int);
 struct __sbuf _ub;
 struct __sFILEX *_extra;
 int _ur;
 unsigned char _ubuf[3];
 unsigned char _nbuf[1];
 struct __sbuf _lb;
 int _blksize;
 fpos_t _offset;
} FILE;
extern FILE *__stdinp;
extern FILE *__stdoutp;
extern FILE *__stderrp;
void clearerr(FILE *);
int fclose(FILE *);
int feof(FILE *);
int ferror(FILE *);
int fflush(FILE *);
int fgetc(FILE *);
int fgetpos(FILE * restrict, fpos_t *);
char *fgets(char * restrict, int, FILE *);
FILE *fopen(const char * restrict, const char * restrict);
int fprintf(FILE * restrict, const char * restrict, ...) ;
int fputc(int, FILE *);
int fputs(const char * restrict, FILE * restrict);
size_t fread(void * restrict, size_t, size_t, FILE * restrict);
FILE *freopen(const char * restrict, const char * restrict,
                 FILE * restrict);
int fscanf(FILE * restrict, const char * restrict, ...) ;
int fseek(FILE *, long, int);
int fsetpos(FILE *, const fpos_t *);
long ftell(FILE *);
size_t fwrite(const void * restrict, size_t, size_t, FILE * restrict);
int getc(FILE *);
int getchar(void);
char *gets(char *);
void perror(const char *);
int printf(const char * restrict, ...) ;
int putc(int, FILE *);
int putchar(int);
int puts(const char *);
int remove(const char *);
int rename (const char *, const char *);
void rewind(FILE *);
int scanf(const char * restrict, ...) ;
void setbuf(FILE * restrict, char * restrict);
int setvbuf(FILE * restrict, char * restrict, int, size_t);
int sprintf(char * restrict, const char * restrict, ...) ;
int sscanf(const char * restrict, const char * restrict, ...) ;
FILE *tmpfile(void);
char *tmpnam(char *);
int ungetc(int, FILE *);
int vfprintf(FILE * restrict, const char * restrict, va_list) ;
int vprintf(const char * restrict, va_list) ;
int vsprintf(char * restrict, const char * restrict, va_list) ;
char *ctermid(char *);
FILE *fdopen(int, const char *);
int fileno(FILE *);
int pclose(FILE *);
FILE *popen(const char *, const char *);
int __srget(FILE *);
int __svfscanf(FILE *, const char *, va_list) ;
int __swbuf(int, FILE *);
void flockfile(FILE *);
int ftrylockfile(FILE *);
void funlockfile(FILE *);
int getc_unlocked(FILE *);
int getchar_unlocked(void);
int putc_unlocked(int, FILE *);
int putchar_unlocked(int);
int getw(FILE *);
int putw(int, FILE *);
char *tempnam(const char *, const char *);
int fseeko(FILE *, off_t, int);
off_t ftello(FILE *);
int snprintf(char * restrict, size_t, const char * restrict, ...) ;
int vfscanf(FILE * restrict, const char * restrict, va_list) ;
int vscanf(const char * restrict, va_list) ;
int vsnprintf(char * restrict, size_t, const char * restrict, va_list) ;
int vsscanf(const char * restrict, const char * restrict, va_list) ;
int dprintf(int, const char * restrict, ...) ;
int vdprintf(int, const char * restrict, va_list) ;
ssize_t getdelim(char ** restrict, size_t * restrict, int, FILE * restrict) ;
ssize_t getline(char ** restrict, size_t * restrict, FILE * restrict) ;
extern const int sys_nerr;
extern const char *const sys_errlist[];
int asprintf(char ** restrict, const char * restrict, ...) ;
char *ctermid_r(char *);
char *fgetln(FILE *, size_t *);
const char *fmtcheck(const char *, const char *);
int fpurge(FILE *);
void setbuffer(FILE *, char *, int);
int setlinebuf(FILE *);
int vasprintf(char ** restrict, const char * restrict, va_list) ;
FILE *zopen(const char *, const char *, int);
FILE *funopen(const void *,
                 int (*)(void *, char *, int),
                 int (*)(void *, const char *, int),
                 fpos_t (*)(void *, fpos_t, int),
                 int (*)(void *));
extern int __sprintf_chk (char * restrict, int, size_t,
     const char * restrict, ...);
extern int __snprintf_chk (char * restrict, size_t, int, size_t,
      const char * restrict, ...);
extern int __vsprintf_chk (char * restrict, int, size_t,
      const char * restrict, va_list);
extern int __vsnprintf_chk (char * restrict, size_t, int, size_t,
       const char * restrict, va_list);
struct utsname {
 char sysname[256];
 char nodename[256];
 char release[256];
 char version[256];
 char machine[256];
};
int uname(struct utsname *);
struct dirent { __uint64_t d_ino; __uint64_t d_seekoff; __uint16_t d_reclen; __uint16_t d_namlen; __uint8_t d_type; char d_name[1024]; };
struct _telldir;
typedef struct {
 int __dd_fd;
 long __dd_loc;
 long __dd_size;
 char *__dd_buf;
 int __dd_len;
 long __dd_seek;
 long __dd_rewind;
 int __dd_flags;
 __darwin_pthread_mutex_t __dd_lock;
 struct _telldir *__dd_td;
} DIR;
int closedir(DIR *);
DIR *opendir(const char *);
struct dirent *readdir(DIR *);
int readdir_r(DIR *, struct dirent *, struct dirent **);
void rewinddir(DIR *);
void seekdir(DIR *, long);
long telldir(DIR *);
DIR *fdopendir(int);
int alphasort(const struct dirent **, const struct dirent **);
int dirfd(DIR *dirp) ;
int scandir(const char *, struct dirent ***,
    int (*)(const struct dirent *), int (*)(const struct dirent **, const struct dirent **));
int getdirentries(int, char *, int, long *);
DIR *__opendir2(const char *, int);
struct flock {
 off_t l_start;
 off_t l_len;
 pid_t l_pid;
 short l_type;
 short l_whence;
};
struct flocktimeout {
 struct flock fl;
 struct timespec timeout;
};
struct radvisory {
       off_t ra_offset;
       int ra_count;
};
typedef struct fcodeblobs {
 void *f_cd_hash;
 size_t f_hash_size;
 void *f_cd_buffer;
 size_t f_cd_size;
 unsigned int *f_out_size;
 int f_arch;
 int __padding;
} fcodeblobs_t;
typedef struct fsignatures {
 off_t fs_file_start;
 void *fs_blob_start;
 size_t fs_blob_size;
} fsignatures_t;
typedef struct fstore {
 unsigned int fst_flags;
 int fst_posmode;
 off_t fst_offset;
 off_t fst_length;
 off_t fst_bytesalloc;
} fstore_t;
typedef struct fbootstraptransfer {
  off_t fbt_offset;
  size_t fbt_length;
  void *fbt_buffer;
} fbootstraptransfer_t;
struct log2phys {
 unsigned int l2p_flags;
 off_t l2p_contigbytes;
 off_t l2p_devoffset;
};
struct _filesec;
typedef struct _filesec *filesec_t;
typedef enum {
 FILESEC_OWNER = 1,
 FILESEC_GROUP = 2,
 FILESEC_UUID = 3,
 FILESEC_MODE = 4,
 FILESEC_ACL = 5,
 FILESEC_GRPUUID = 6,
 FILESEC_ACL_RAW = 100,
 FILESEC_ACL_ALLOCSIZE = 101
} filesec_property_t;
int open(const char *, int, ...);
int openat(int, const char *, int, ...);
int creat(const char *, mode_t);
int fcntl(int, int, ...);
int openx_np(const char *, int, filesec_t);
int open_dprotected_np ( const char *, int, int, int, ...);
int flock(int, int);
filesec_t filesec_init(void);
filesec_t filesec_dup(filesec_t);
void filesec_free(filesec_t);
int filesec_get_property(filesec_t, filesec_property_t, void *);
int filesec_query_property(filesec_t, filesec_property_t, int *);
int filesec_set_property(filesec_t, filesec_property_t, const void *);
int filesec_unset_property(filesec_t, filesec_property_t) ;
typedef struct {
 void *dptr;
 size_t dsize;
} datum;
typedef struct {
    char __opaque[sizeof(int) + 8 * sizeof(void *)];
} DBM;
int dbm_clearerr( DBM *);
void dbm_close(DBM *);
int dbm_delete(DBM *, datum);
int dbm_dirfno(DBM *);
int dbm_error( DBM *);
datum dbm_fetch(DBM *, datum);
datum dbm_firstkey(DBM *);
long dbm_forder(DBM *, datum);
datum dbm_nextkey(DBM *);
DBM *dbm_open(const char *, int, mode_t);
int dbm_store(DBM *, datum, datum, int);
typedef enum {
 P_ALL,
 P_PID,
 P_PGID
} idtype_t;
typedef __uint64_t rlim_t;
struct rusage {
 struct timeval ru_utime;
 struct timeval ru_stime;
 long ru_maxrss;
 long ru_ixrss;
 long ru_idrss;
 long ru_isrss;
 long ru_minflt;
 long ru_majflt;
 long ru_nswap;
 long ru_inblock;
 long ru_oublock;
 long ru_msgsnd;
 long ru_msgrcv;
 long ru_nsignals;
 long ru_nvcsw;
 long ru_nivcsw;
};
typedef void *rusage_info_t;
struct rusage_info_v0 {
 uint8_t ri_uuid[16];
 uint64_t ri_user_time;
 uint64_t ri_system_time;
 uint64_t ri_pkg_idle_wkups;
 uint64_t ri_interrupt_wkups;
 uint64_t ri_pageins;
 uint64_t ri_wired_size;
 uint64_t ri_resident_size;
 uint64_t ri_phys_footprint;
 uint64_t ri_proc_start_abstime;
 uint64_t ri_proc_exit_abstime;
};
struct rusage_info_v1 {
 uint8_t ri_uuid[16];
 uint64_t ri_user_time;
 uint64_t ri_system_time;
 uint64_t ri_pkg_idle_wkups;
 uint64_t ri_interrupt_wkups;
 uint64_t ri_pageins;
 uint64_t ri_wired_size;
 uint64_t ri_resident_size;
 uint64_t ri_phys_footprint;
 uint64_t ri_proc_start_abstime;
 uint64_t ri_proc_exit_abstime;
 uint64_t ri_child_user_time;
 uint64_t ri_child_system_time;
 uint64_t ri_child_pkg_idle_wkups;
 uint64_t ri_child_interrupt_wkups;
 uint64_t ri_child_pageins;
 uint64_t ri_child_elapsed_abstime;
};
struct rusage_info_v2 {
 uint8_t ri_uuid[16];
 uint64_t ri_user_time;
 uint64_t ri_system_time;
 uint64_t ri_pkg_idle_wkups;
 uint64_t ri_interrupt_wkups;
 uint64_t ri_pageins;
 uint64_t ri_wired_size;
 uint64_t ri_resident_size;
 uint64_t ri_phys_footprint;
 uint64_t ri_proc_start_abstime;
 uint64_t ri_proc_exit_abstime;
 uint64_t ri_child_user_time;
 uint64_t ri_child_system_time;
 uint64_t ri_child_pkg_idle_wkups;
 uint64_t ri_child_interrupt_wkups;
 uint64_t ri_child_pageins;
 uint64_t ri_child_elapsed_abstime;
 uint64_t ri_diskio_bytesread;
 uint64_t ri_diskio_byteswritten;
};
struct rusage_info_v3 {
 uint8_t ri_uuid[16];
 uint64_t ri_user_time;
 uint64_t ri_system_time;
 uint64_t ri_pkg_idle_wkups;
 uint64_t ri_interrupt_wkups;
 uint64_t ri_pageins;
 uint64_t ri_wired_size;
 uint64_t ri_resident_size;
 uint64_t ri_phys_footprint;
 uint64_t ri_proc_start_abstime;
 uint64_t ri_proc_exit_abstime;
 uint64_t ri_child_user_time;
 uint64_t ri_child_system_time;
 uint64_t ri_child_pkg_idle_wkups;
 uint64_t ri_child_interrupt_wkups;
 uint64_t ri_child_pageins;
 uint64_t ri_child_elapsed_abstime;
 uint64_t ri_diskio_bytesread;
 uint64_t ri_diskio_byteswritten;
 uint64_t ri_cpu_time_qos_default;
 uint64_t ri_cpu_time_qos_maintenance;
 uint64_t ri_cpu_time_qos_background;
 uint64_t ri_cpu_time_qos_utility;
 uint64_t ri_cpu_time_qos_legacy;
 uint64_t ri_cpu_time_qos_user_initiated;
 uint64_t ri_cpu_time_qos_user_interactive;
 uint64_t ri_billed_system_time;
 uint64_t ri_serviced_system_time;
};
typedef struct rusage_info_v3 rusage_info_current;
struct rlimit {
 rlim_t rlim_cur;
 rlim_t rlim_max;
};
struct proc_rlimit_control_wakeupmon {
 uint32_t wm_flags;
 int32_t wm_rate;
};
int getpriority(int, id_t);
int getiopolicy_np(int, int) ;
int getrlimit(int, struct rlimit *);
int getrusage(int, struct rusage *);
int setpriority(int, id_t, int);
int setiopolicy_np(int, int, int) ;
int setrlimit(int, const struct rlimit *);
union wait {
 int w_status;
 struct {
  unsigned int w_Termsig:7,
    w_Coredump:1,
    w_Retcode:8,
    w_Filler:16;
 } w_T;
 struct {
  unsigned int w_Stopval:8,
    w_Stopsig:8,
    w_Filler:16;
 } w_S;
};
pid_t wait(int *);
pid_t waitpid(pid_t, int *, int);
int waitid(idtype_t, id_t, siginfo_t *, int);
pid_t wait3(int *, int, struct rusage *);
pid_t wait4(pid_t, int *, int, struct rusage *);
void *alloca(size_t);
typedef struct {
 int quot;
 int rem;
} div_t;
typedef struct {
 long quot;
 long rem;
} ldiv_t;
typedef struct {
 long long quot;
 long long rem;
} lldiv_t;
extern int __mb_cur_max;
void abort(void) ;
int abs(int) ;
int atexit(void (*)(void));
double atof(const char *);
int atoi(const char *);
long atol(const char *);
long long
  atoll(const char *);
void *bsearch(const void *, const void *, size_t,
     size_t, int (*)(const void *, const void *));
void *calloc(size_t, size_t);
div_t div(int, int) ;
void exit(int) ;
void free(void *);
char *getenv(const char *);
long labs(long) ;
ldiv_t ldiv(long, long) ;
long long
  llabs(long long);
lldiv_t lldiv(long long, long long);
void *malloc(size_t);
int mblen(const char *, size_t);
size_t mbstowcs(wchar_t * restrict , const char * restrict, size_t);
int mbtowc(wchar_t * restrict, const char * restrict, size_t);
int posix_memalign(void **, size_t, size_t) ;
void qsort(void *, size_t, size_t,
     int (*)(const void *, const void *));
int rand(void);
void *realloc(void *, size_t);
void srand(unsigned);
double strtod(const char *, char **);
float strtof(const char *, char **);
long strtol(const char *, char **, int);
long double
  strtold(const char *, char **);
long long
  strtoll(const char *, char **, int);
unsigned long
  strtoul(const char *, char **, int);
unsigned long long
  strtoull(const char *, char **, int);
int system(const char *);
size_t wcstombs(char * restrict, const wchar_t * restrict, size_t);
int wctomb(char *, wchar_t);
void _Exit(int) ;
long a64l(const char *);
double drand48(void);
char *ecvt(double, int, int *restrict, int *restrict);
double erand48(unsigned short[3]);
char *fcvt(double, int, int *restrict, int *restrict);
char *gcvt(double, int, char *);
int getsubopt(char **, char * const *, char **);
int grantpt(int);
char *initstate(unsigned, char *, size_t);
long jrand48(unsigned short[3]);
char *l64a(long);
void lcong48(unsigned short[7]);
long lrand48(void);
char *mktemp(char *);
int mkstemp(char *);
long mrand48(void);
long nrand48(unsigned short[3]);
int posix_openpt(int);
char *ptsname(int);
int putenv(char *);
long random(void);
int rand_r(unsigned *);
char *realpath(const char * restrict, char * restrict);
unsigned short
 *seed48(unsigned short[3]);
int setenv(const char *, const char *, int);
void setkey(const char *);
char *setstate(const char *);
void srand48(long);
void srandom(unsigned);
int unlockpt(int);
int unsetenv(const char *);
u_int32_t arc4random(void);
void arc4random_addrandom(unsigned char * , int );
void arc4random_buf(void * , size_t ) ;
void arc4random_stir(void);
u_int32_t
  arc4random_uniform(u_int32_t ) ;
char *cgetcap(char *, const char *, int);
int cgetclose(void);
int cgetent(char **, char **, const char *);
int cgetfirst(char **, char **);
int cgetmatch(const char *, const char *);
int cgetnext(char **, char **);
int cgetnum(char *, const char *, long *);
int cgetset(const char *);
int cgetstr(char *, const char *, char **);
int cgetustr(char *, const char *, char **);
int daemon(int, int);
char *devname(dev_t, mode_t);
char *devname_r(dev_t, mode_t, char *buf, int len);
char *getbsize(int *, long *);
int getloadavg(double [], int);
const char
 *getprogname(void);
int heapsort(void *, size_t, size_t,
     int (*)(const void *, const void *));
int mergesort(void *, size_t, size_t,
     int (*)(const void *, const void *));
void psort(void *, size_t, size_t,
     int (*)(const void *, const void *)) ;
void psort_r(void *, size_t, size_t, void *,
     int (*)(void *, const void *, const void *)) ;
void qsort_r(void *, size_t, size_t, void *,
     int (*)(void *, const void *, const void *));
int radixsort(const unsigned char **, int, const unsigned char *,
     unsigned);
void setprogname(const char *);
int sradixsort(const unsigned char **, int, const unsigned char *,
     unsigned);
void sranddev(void);
void srandomdev(void);
void *reallocf(void *, size_t);
long long
  strtoq(const char *, char **, int);
unsigned long long
  strtouq(const char *, char **, int);
extern char *suboptarg;
void *valloc(size_t);
typedef struct dl_info {
        const char *dli_fname;
        void *dli_fbase;
        const char *dli_sname;
        void *dli_saddr;
} Dl_info;
extern int dladdr(const void *, Dl_info *);
extern int dlclose(void * __handle);
extern char * dlerror(void);
extern void * dlopen(const char * __path, int __mode);
extern void * dlsym(void * __handle, const char * __symbol);
extern _Bool dlopen_preflight(const char* __path) ;
struct net_event_data {
 u_int32_t if_family;
 u_int32_t if_unit;
 char if_name[16];
};
struct timeval32
{
 __int32_t tv_sec;
 __int32_t tv_usec;
};
struct if_data {
 u_char ifi_type;
 u_char ifi_typelen;
 u_char ifi_physical;
 u_char ifi_addrlen;
 u_char ifi_hdrlen;
 u_char ifi_recvquota;
 u_char ifi_xmitquota;
 u_char ifi_unused1;
 u_int32_t ifi_mtu;
 u_int32_t ifi_metric;
 u_int32_t ifi_baudrate;
 u_int32_t ifi_ipackets;
 u_int32_t ifi_ierrors;
 u_int32_t ifi_opackets;
 u_int32_t ifi_oerrors;
 u_int32_t ifi_collisions;
 u_int32_t ifi_ibytes;
 u_int32_t ifi_obytes;
 u_int32_t ifi_imcasts;
 u_int32_t ifi_omcasts;
 u_int32_t ifi_iqdrops;
 u_int32_t ifi_noproto;
 u_int32_t ifi_recvtiming;
 u_int32_t ifi_xmittiming;
 struct timeval32 ifi_lastchange;
 u_int32_t ifi_unused2;
 u_int32_t ifi_hwassist;
 u_int32_t ifi_reserved1;
 u_int32_t ifi_reserved2;
};
struct if_data64 {
 u_char ifi_type;
 u_char ifi_typelen;
 u_char ifi_physical;
 u_char ifi_addrlen;
 u_char ifi_hdrlen;
 u_char ifi_recvquota;
 u_char ifi_xmitquota;
 u_char ifi_unused1;
 u_int32_t ifi_mtu;
 u_int32_t ifi_metric;
 u_int64_t ifi_baudrate;
 u_int64_t ifi_ipackets;
 u_int64_t ifi_ierrors;
 u_int64_t ifi_opackets;
 u_int64_t ifi_oerrors;
 u_int64_t ifi_collisions;
 u_int64_t ifi_ibytes;
 u_int64_t ifi_obytes;
 u_int64_t ifi_imcasts;
 u_int64_t ifi_omcasts;
 u_int64_t ifi_iqdrops;
 u_int64_t ifi_noproto;
 u_int32_t ifi_recvtiming;
 u_int32_t ifi_xmittiming;
 struct timeval32 ifi_lastchange;
};
struct ifqueue {
 void *ifq_head;
 void *ifq_tail;
 int ifq_len;
 int ifq_maxlen;
 int ifq_drops;
};
struct if_clonereq {
 int ifcr_total;
 int ifcr_count;
 char *ifcr_buffer;
};
struct if_msghdr {
 unsigned short ifm_msglen;
 unsigned char ifm_version;
 unsigned char ifm_type;
 int ifm_addrs;
 int ifm_flags;
 unsigned short ifm_index;
 struct if_data ifm_data;
};
struct ifa_msghdr {
 unsigned short ifam_msglen;
 unsigned char ifam_version;
 unsigned char ifam_type;
 int ifam_addrs;
 int ifam_flags;
 unsigned short ifam_index;
 int ifam_metric;
};
struct ifma_msghdr {
 unsigned short ifmam_msglen;
 unsigned char ifmam_version;
 unsigned char ifmam_type;
 int ifmam_addrs;
 int ifmam_flags;
 unsigned short ifmam_index;
};
struct if_msghdr2 {
 u_short ifm_msglen;
 u_char ifm_version;
 u_char ifm_type;
 int ifm_addrs;
 int ifm_flags;
 u_short ifm_index;
 int ifm_snd_len;
 int ifm_snd_maxlen;
 int ifm_snd_drops;
 int ifm_timer;
 struct if_data64 ifm_data;
};
struct ifma_msghdr2 {
 u_short ifmam_msglen;
 u_char ifmam_version;
 u_char ifmam_type;
 int ifmam_addrs;
 int ifmam_flags;
 u_short ifmam_index;
 int32_t ifmam_refcount;
};
struct ifdevmtu {
 int ifdm_current;
 int ifdm_min;
 int ifdm_max;
};
struct ifkpi {
 unsigned int ifk_module_id;
 unsigned int ifk_type;
 union {
  void *ifk_ptr;
  int ifk_value;
 } ifk_data;
};
struct ifreq {
 char ifr_name[16];
 union {
  struct sockaddr ifru_addr;
  struct sockaddr ifru_dstaddr;
  struct sockaddr ifru_broadaddr;
  short ifru_flags;
  int ifru_metric;
  int ifru_mtu;
  int ifru_phys;
  int ifru_media;
  int ifru_intval;
  caddr_t ifru_data;
  struct ifdevmtu ifru_devmtu;
  struct ifkpi ifru_kpi;
  u_int32_t ifru_wake_flags;
  u_int32_t ifru_route_refcnt;
  int ifru_cap[2];
 } ifr_ifru;
};
struct ifaliasreq {
 char ifra_name[16];
 struct sockaddr ifra_addr;
 struct sockaddr ifra_broadaddr;
 struct sockaddr ifra_mask;
};
struct rslvmulti_req {
 struct sockaddr *sa;
 struct sockaddr **llsa;
};
struct ifmediareq {
 char ifm_name[16];
 int ifm_current;
 int ifm_mask;
 int ifm_status;
 int ifm_active;
 int ifm_count;
 int *ifm_ulist;
};
struct ifdrv {
 char ifd_name[16];
 unsigned long ifd_cmd;
 size_t ifd_len;
 void *ifd_data;
};
struct ifstat {
 char ifs_name[16];
 char ascii[800 + 1];
};
struct ifconf {
 int ifc_len;
 union {
  caddr_t ifcu_buf;
  struct ifreq *ifcu_req;
 } ifc_ifcu;
};
struct kev_dl_proto_data {
 struct net_event_data link_data;
 u_int32_t proto_family;
 u_int32_t proto_remaining_count;
};
struct if_nameindex {
 unsigned int if_index;
 char *if_name;
};
unsigned int if_nametoindex(const char *);
char *if_indextoname(unsigned int, char *);
struct if_nameindex *if_nameindex(void);
void if_freenameindex(struct if_nameindex *);
void *memchr(const void *, int, size_t);
int memcmp(const void *, const void *, size_t);
void *memcpy(void *, const void *, size_t);
void *memmove(void *, const void *, size_t);
void *memset(void *, int, size_t);
char *strcat(char *, const char *);
char *strchr(const char *, int);
int strcmp(const char *, const char *);
int strcoll(const char *, const char *);
char *strcpy(char *, const char *);
size_t strcspn(const char *, const char *);
char *strerror(int);
size_t strlen(const char *);
char *strncat(char *, const char *, size_t);
int strncmp(const char *, const char *, size_t);
char *strncpy(char *, const char *, size_t);
char *strpbrk(const char *, const char *);
char *strrchr(const char *, int);
size_t strspn(const char *, const char *);
char *strstr(const char *, const char *);
char *strtok(char *, const char *);
size_t strxfrm(char *, const char *, size_t);
char *strtok_r(char *, const char *, char **);
int strerror_r(int, char *, size_t);
char *strdup(const char *);
void *memccpy(void *, const void *, int, size_t);
char *stpcpy(char *, const char *);
char *stpncpy(char *, const char *, size_t) ;
char *strndup(const char *, size_t) ;
size_t strnlen(const char *, size_t) ;
char *strsignal(int sig);
errno_t memset_s(void *, rsize_t, int, rsize_t) ;
void *memmem(const void *, size_t, const void *, size_t) ;
void memset_pattern4(void *, const void *, size_t) ;
void memset_pattern8(void *, const void *, size_t) ;
void memset_pattern16(void *, const void *, size_t) ;
char *strcasestr(const char *, const char *);
char *strnstr(const char *, const char *, size_t);
size_t strlcat(char *, const char *, size_t);
size_t strlcpy(char *, const char *, size_t);
void strmode(int, char *);
char *strsep(char **, const char *);
void swab(const void * restrict, void * restrict, ssize_t);
int bcmp(const void *, const void *, size_t) ;
void bcopy(const void *, void *, size_t) ;
void bzero(void *, size_t) ;
char *index(const char *, int) ;
char *rindex(const char *, int) ;
int ffs(int);
int strcasecmp(const char *, const char *);
int strncasecmp(const char *, const char *, size_t);
int ffsl(long) ;
int ffsll(long long) ;
int fls(int) ;
int flsl(long) ;
int flsll(long long) ;
void closelog(void);
void openlog(const char *, int, int);
int setlogmask(int);
void syslog(int, const char *, ...) ;
void vsyslog(int, const char *, __darwin_va_list) ;
extern int * __error(void);
extern int h_errno;
struct hostent {
 char *h_name;
 char **h_aliases;
 int h_addrtype;
 int h_length;
 char **h_addr_list;
};
struct netent {
 char *n_name;
 char **n_aliases;
 int n_addrtype;
 uint32_t n_net;
};
struct servent {
 char *s_name;
 char **s_aliases;
 int s_port;
 char *s_proto;
};
struct protoent {
 char *p_name;
 char **p_aliases;
 int p_proto;
};
struct addrinfo {
 int ai_flags;
 int ai_family;
 int ai_socktype;
 int ai_protocol;
 socklen_t ai_addrlen;
 char *ai_canonname;
 struct sockaddr *ai_addr;
 struct addrinfo *ai_next;
};
struct rpcent {
        char *r_name;
        char **r_aliases;
        int r_number;
};
void endhostent(void);
void endnetent(void);
void endprotoent(void);
void endservent(void);
void freeaddrinfo(struct addrinfo *);
const char *gai_strerror(int);
int getaddrinfo(const char * restrict, const char * restrict,
       const struct addrinfo * restrict,
       struct addrinfo ** restrict);
struct hostent *gethostbyaddr(const void *, socklen_t, int);
struct hostent *gethostbyname(const char *);
struct hostent *gethostent(void);
int getnameinfo(const struct sockaddr * restrict, socklen_t,
         char * restrict, socklen_t, char * restrict,
         socklen_t, int);
struct netent *getnetbyaddr(uint32_t, int);
struct netent *getnetbyname(const char *);
struct netent *getnetent(void);
struct protoent *getprotobyname(const char *);
struct protoent *getprotobynumber(int);
struct protoent *getprotoent(void);
struct servent *getservbyname(const char *, const char *);
struct servent *getservbyport(int, const char *);
struct servent *getservent(void);
void sethostent(int);
void setnetent(int);
void setprotoent(int);
void setservent(int);
void freehostent(struct hostent *);
struct hostent *gethostbyname2(const char *, int);
struct hostent *getipnodebyaddr(const void *, size_t, int, int *);
struct hostent *getipnodebyname(const char *, int, int, int *);
struct rpcent *getrpcbyname(const char *name);
struct rpcent *getrpcbynumber(int number);
struct rpcent *getrpcent(void);
void setrpcent(int stayopen);
void endrpcent(void);
void herror(const char *);
const char *hstrerror(int);
int innetgr(const char *, const char *, const char *, const char *);
int getnetgrent(char **, char **, char **);
void endnetgrent(void);
void setnetgrent(const char *);
typedef unsigned long tcflag_t;
typedef unsigned char cc_t;
typedef unsigned long speed_t;
struct termios {
 tcflag_t c_iflag;
 tcflag_t c_oflag;
 tcflag_t c_cflag;
 tcflag_t c_lflag;
 cc_t c_cc[20];
 speed_t c_ispeed;
 speed_t c_ospeed;
};
speed_t cfgetispeed(const struct termios *);
speed_t cfgetospeed(const struct termios *);
int cfsetispeed(struct termios *, speed_t);
int cfsetospeed(struct termios *, speed_t);
int tcgetattr(int, struct termios *);
int tcsetattr(int, int, const struct termios *);
int tcdrain(int);
int tcflow(int, int);
int tcflush(int, int);
int tcsendbreak(int, int);
void cfmakeraw(struct termios *);
int cfsetspeed(struct termios *, speed_t);
struct winsize {
 unsigned short ws_row;
 unsigned short ws_col;
 unsigned short ws_xpixel;
 unsigned short ws_ypixel;
};
pid_t tcgetsid(int);
typedef struct {
    unsigned short __control;
    unsigned short __status;
    unsigned int __mxcsr;
    char __reserved[8];
} fenv_t;
typedef unsigned short fexcept_t;
extern const fenv_t _FE_DFL_ENV;
extern const fenv_t _FE_DFL_DISABLE_SSE_DENORMS_ENV;
extern int feclearexcept(int );
extern int fegetexceptflag(fexcept_t * , int );
extern int feraiseexcept(int );
extern int fesetexceptflag(const fexcept_t * , int );
extern int fetestexcept(int );
extern int fegetround(void);
extern int fesetround(int );
extern int fegetenv(fenv_t * );
extern int feholdexcept(fenv_t * );
extern int fesetenv(const fenv_t * );
extern int feupdateenv(const fenv_t * );
typedef __uint32_t tcp_seq;
typedef __uint32_t tcp_cc;
struct tcphdr {
 unsigned short th_sport;
 unsigned short th_dport;
 tcp_seq th_seq;
 tcp_seq th_ack;
 unsigned int th_x2:4,
   th_off:4;
 unsigned char th_flags;
 unsigned short th_win;
 unsigned short th_sum;
 unsigned short th_urp;
};
struct ipc_perm
{
 uid_t uid;
 gid_t gid;
 uid_t cuid;
 gid_t cgid;
 mode_t mode;
 unsigned short _seq;
 key_t _key;
};
key_t ftok(const char *, int);
typedef struct __nl_cat_d {
 void *__data;
 int __size;
} *nl_catd;
typedef __darwin_nl_item nl_item;
nl_catd catopen(const char *, int);
char *catgets(nl_catd, int, int, const char *);
int catclose(nl_catd);
int mlockall(int);
int munlockall(void);
int mlock(const void *, size_t);
void * mmap(void *, size_t, int, int, int, off_t);
int mprotect(void *, size_t, int);
int msync(void *, size_t, int);
int munlock(const void *, size_t);
int munmap(void *, size_t);
int shm_open(const char *, int, ...);
int shm_unlink(const char *);
int posix_madvise(void *, size_t, int);
int madvise(void *, size_t, int);
int mincore(const void *, size_t, char *);
int minherit(void *, size_t, int);
int fmtmsg(long, const char *, int, const char *, const char *,
     const char *);
struct pollfd
{
 int fd;
 short events;
 short revents;
};
typedef unsigned int nfds_t;
extern int poll (struct pollfd *, nfds_t, int);
typedef unsigned long msgqnum_t;
typedef unsigned long msglen_t;
struct __msqid_ds_new
{
 struct ipc_perm msg_perm;
 __int32_t msg_first;
 __int32_t msg_last;
 msglen_t msg_cbytes;
 msgqnum_t msg_qnum;
 msglen_t msg_qbytes;
 pid_t msg_lspid;
 pid_t msg_lrpid;
 time_t msg_stime;
 __int32_t msg_pad1;
 time_t msg_rtime;
 __int32_t msg_pad2;
 time_t msg_ctime;
 __int32_t msg_pad3;
 __int32_t msg_pad4[4];
};
struct msg {
 struct msg *msg_next;
 long msg_type;
 unsigned short msg_ts;
 short msg_spot;
 struct label *label;
};
struct mymsg {
 long mtype;
 char mtext[1];
};
struct msginfo {
 int msgmax,
  msgmni,
  msgmnb,
  msgtql,
  msgssz,
  msgseg;
};
int msgsys(int, ...);
int msgctl(int, int, struct __msqid_ds_new *);
int msgget(key_t, int);
ssize_t msgrcv(int, void *, size_t, long, int);
int msgsnd(int, const void *, size_t, int);
int fnmatch(const char *, const char *, int);
struct sched_param { int sched_priority; char __opaque[4]; };
extern int sched_yield(void);
extern int sched_get_priority_min(int);
extern int sched_get_priority_max(int);
enum { QOS_CLASS_USER_INTERACTIVE = 0x21,
 QOS_CLASS_USER_INITIATED = 0x19,
 QOS_CLASS_DEFAULT = 0x15,
 QOS_CLASS_UTILITY = 0x11,
 QOS_CLASS_BACKGROUND = 0x09,
 QOS_CLASS_UNSPECIFIED = 0x00,
 };
typedef unsigned int qos_class_t;
qos_class_t
qos_class_self(void);
qos_class_t
qos_class_main(void);
int
pthread_attr_set_qos_class_np(pthread_attr_t *__attr,
  qos_class_t __qos_class, int __relative_priority);
int
pthread_attr_get_qos_class_np(pthread_attr_t * restrict __attr,
  qos_class_t * restrict __qos_class,
  int * restrict __relative_priority);
int
pthread_set_qos_class_self_np(qos_class_t __qos_class,
  int __relative_priority);
int
pthread_get_qos_class_np(pthread_t __pthread,
  qos_class_t * restrict __qos_class,
  int * restrict __relative_priority);
typedef struct pthread_override_s* pthread_override_t;
pthread_override_t
pthread_override_qos_class_start_np(pthread_t __pthread,
  qos_class_t __qos_class, int __relative_priority);
int
pthread_override_qos_class_end_np(pthread_override_t __override);

int pthread_atfork(void (*)(void), void (*)(void), void (*)(void));

int pthread_attr_destroy(pthread_attr_t *);

int pthread_attr_getdetachstate(const pthread_attr_t *, int *);

int pthread_attr_getguardsize(const pthread_attr_t * restrict, size_t * restrict);

int pthread_attr_getinheritsched(const pthread_attr_t * restrict, int * restrict);

int pthread_attr_getschedparam(const pthread_attr_t * restrict,
  struct sched_param * restrict);

int pthread_attr_getschedpolicy(const pthread_attr_t * restrict, int * restrict);

int pthread_attr_getscope(const pthread_attr_t * restrict, int * restrict);

int pthread_attr_getstack(const pthread_attr_t * restrict, void ** restrict,
  size_t * restrict);

int pthread_attr_getstackaddr(const pthread_attr_t * restrict, void ** restrict);

int pthread_attr_getstacksize(const pthread_attr_t * restrict, size_t * restrict);

int pthread_attr_init(pthread_attr_t *);

int pthread_attr_setdetachstate(pthread_attr_t *, int);

int pthread_attr_setguardsize(pthread_attr_t *, size_t);

int pthread_attr_setinheritsched(pthread_attr_t *, int);

int pthread_attr_setschedparam(pthread_attr_t * restrict,
  const struct sched_param * restrict);

int pthread_attr_setschedpolicy(pthread_attr_t *, int);

int pthread_attr_setscope(pthread_attr_t *, int);

int pthread_attr_setstack(pthread_attr_t *, void *, size_t);

int pthread_attr_setstackaddr(pthread_attr_t *, void *);

int pthread_attr_setstacksize(pthread_attr_t *, size_t);

int pthread_cancel(pthread_t);

int pthread_cond_broadcast(pthread_cond_t *);

int pthread_cond_destroy(pthread_cond_t *);

int pthread_cond_init(pthread_cond_t * restrict,
  const pthread_condattr_t * restrict);

int pthread_cond_signal(pthread_cond_t *);

int pthread_cond_timedwait(pthread_cond_t * restrict, pthread_mutex_t * restrict,
  const struct timespec * restrict);

int pthread_cond_wait(pthread_cond_t * restrict,
  pthread_mutex_t * restrict);

int pthread_condattr_destroy(pthread_condattr_t *);

int pthread_condattr_init(pthread_condattr_t *);

int pthread_condattr_getpshared(const pthread_condattr_t * restrict,
  int * restrict);

int pthread_condattr_setpshared(pthread_condattr_t *, int);

int pthread_create(pthread_t * restrict, const pthread_attr_t * restrict,
  void *(*)(void *), void * restrict);

int pthread_detach(pthread_t);

int pthread_equal(pthread_t, pthread_t);

void pthread_exit(void *) ;

int pthread_getconcurrency(void);

int pthread_getschedparam(pthread_t , int * restrict,
  struct sched_param * restrict);

void* pthread_getspecific(pthread_key_t);

int pthread_join(pthread_t , void **);

int pthread_key_create(pthread_key_t *, void (*)(void *));

int pthread_key_delete(pthread_key_t);

int pthread_mutex_destroy(pthread_mutex_t *);

int pthread_mutex_getprioceiling(const pthread_mutex_t * restrict,
  int * restrict);

int pthread_mutex_init(pthread_mutex_t * restrict,
  const pthread_mutexattr_t * restrict);

int pthread_mutex_lock(pthread_mutex_t *);

int pthread_mutex_setprioceiling(pthread_mutex_t * restrict, int,
  int * restrict);

int pthread_mutex_trylock(pthread_mutex_t *);

int pthread_mutex_unlock(pthread_mutex_t *);

int pthread_mutexattr_destroy(pthread_mutexattr_t *);

int pthread_mutexattr_getprioceiling(const pthread_mutexattr_t * restrict,
  int * restrict);

int pthread_mutexattr_getprotocol(const pthread_mutexattr_t * restrict,
  int * restrict);

int pthread_mutexattr_getpshared(const pthread_mutexattr_t * restrict,
  int * restrict);

int pthread_mutexattr_gettype(const pthread_mutexattr_t * restrict,
  int * restrict);

int pthread_mutexattr_init(pthread_mutexattr_t *);

int pthread_mutexattr_setprioceiling(pthread_mutexattr_t *, int);

int pthread_mutexattr_setprotocol(pthread_mutexattr_t *, int);

int pthread_mutexattr_setpshared(pthread_mutexattr_t *, int);

int pthread_mutexattr_settype(pthread_mutexattr_t *, int);

int pthread_once(pthread_once_t *, void (*)(void));

int pthread_rwlock_destroy(pthread_rwlock_t * );

int pthread_rwlock_init(pthread_rwlock_t * restrict,
  const pthread_rwlockattr_t * restrict);

int pthread_rwlock_rdlock(pthread_rwlock_t *);

int pthread_rwlock_tryrdlock(pthread_rwlock_t *);

int pthread_rwlock_trywrlock(pthread_rwlock_t *);

int pthread_rwlock_wrlock(pthread_rwlock_t *);

int pthread_rwlock_unlock(pthread_rwlock_t *);

int pthread_rwlockattr_destroy(pthread_rwlockattr_t *);

int pthread_rwlockattr_getpshared(const pthread_rwlockattr_t * restrict,
  int * restrict);

int pthread_rwlockattr_init(pthread_rwlockattr_t *);

int pthread_rwlockattr_setpshared(pthread_rwlockattr_t *, int);

pthread_t pthread_self(void);

int pthread_setcancelstate(int , int *);

int pthread_setcanceltype(int , int *);

int pthread_setconcurrency(int);

int pthread_setschedparam(pthread_t, int, const struct sched_param *);

int pthread_setspecific(pthread_key_t , const void *);

void pthread_testcancel(void);

int pthread_is_threaded_np(void);

int pthread_threadid_np(pthread_t,__uint64_t*);

int pthread_getname_np(pthread_t,char*,size_t);

int pthread_setname_np(const char*);

int pthread_main_np(void);

mach_port_t pthread_mach_thread_np(pthread_t);

size_t pthread_get_stacksize_np(pthread_t);

void* pthread_get_stackaddr_np(pthread_t);

int pthread_cond_signal_thread_np(pthread_cond_t *, pthread_t);

int pthread_cond_timedwait_relative_np(pthread_cond_t *, pthread_mutex_t *,
  const struct timespec *);

int pthread_create_suspended_np(pthread_t *, const pthread_attr_t *,
  void *(*)(void *), void *);

int pthread_kill(pthread_t, int);

pthread_t pthread_from_mach_thread_np(mach_port_t);

int pthread_sigmask(int, const sigset_t *, sigset_t *);

void pthread_yield_np(void);
long ulimit(int, ...);
struct ostat {
 __uint16_t st_dev;
 ino_t st_ino;
 mode_t st_mode;
 nlink_t st_nlink;
 __uint16_t st_uid;
 __uint16_t st_gid;
 __uint16_t st_rdev;
 __int32_t st_size;
 struct timespec st_atimespec;
 struct timespec st_mtimespec;
 struct timespec st_ctimespec;
 __int32_t st_blksize;
 __int32_t st_blocks;
 __uint32_t st_flags;
 __uint32_t st_gen;
};
struct stat { dev_t st_dev; mode_t st_mode; nlink_t st_nlink; __darwin_ino64_t st_ino; uid_t st_uid; gid_t st_gid; dev_t st_rdev; struct timespec st_atimespec; struct timespec st_mtimespec; struct timespec st_ctimespec; struct timespec st_birthtimespec; off_t st_size; blkcnt_t st_blocks; blksize_t st_blksize; __uint32_t st_flags; __uint32_t st_gen; __int32_t st_lspare; __int64_t st_qspare[2]; };
struct stat64 { dev_t st_dev; mode_t st_mode; nlink_t st_nlink; __darwin_ino64_t st_ino; uid_t st_uid; gid_t st_gid; dev_t st_rdev; struct timespec st_atimespec; struct timespec st_mtimespec; struct timespec st_ctimespec; struct timespec st_birthtimespec; off_t st_size; blkcnt_t st_blocks; blksize_t st_blksize; __uint32_t st_flags; __uint32_t st_gen; __int32_t st_lspare; __int64_t st_qspare[2]; };
int chmod(const char *, mode_t);
int fchmod(int, mode_t);
int fstat(int, struct stat *);
int lstat(const char *, struct stat *);
int mkdir(const char *, mode_t);
int mkfifo(const char *, mode_t);
int stat(const char *, struct stat *);
int mknod(const char *, mode_t, dev_t);
mode_t umask(mode_t);
int fchmodat(int, const char *, mode_t, int) ;
int fstatat(int, const char *, struct stat *, int);
int mkdirat(int, const char *, mode_t) ;
int chflags(const char *, __uint32_t);
int chmodx_np(const char *, filesec_t);
int fchflags(int, __uint32_t);
int fchmodx_np(int, filesec_t);
int fstatx_np(int, struct stat *, filesec_t);
int lchflags(const char *, __uint32_t) ;
int lchmod(const char *, mode_t) ;
int lstatx_np(const char *, struct stat *, filesec_t);
int mkdirx_np(const char *, filesec_t);
int mkfifox_np(const char *, filesec_t);
int statx_np(const char *, struct stat *, filesec_t);
int umaskx_np(filesec_t) ;
int fstatx64_np(int, struct stat64 *, filesec_t) ;
int lstatx64_np(const char *, struct stat64 *, filesec_t) ;
int statx64_np(const char *, struct stat64 *, filesec_t) ;
int fstat64(int, struct stat64 *) ;
int lstat64(const char *, struct stat64 *) ;
int stat64(const char *, struct stat64 *) ;
struct FTW {
 int base;
 int level;
};
int ftw(const char *, int (*)(const char *, const struct stat *, int), int);

int nftw(const char *, int (*)(const char *, const struct stat *, int,
     struct FTW *), int, int);
struct passwd {
 char *pw_name;
 char *pw_passwd;
 uid_t pw_uid;
 gid_t pw_gid;
 __darwin_time_t pw_change;
 char *pw_class;
 char *pw_gecos;
 char *pw_dir;
 char *pw_shell;
 __darwin_time_t pw_expire;
};
struct passwd *getpwuid(uid_t);
struct passwd *getpwnam(const char *);
int getpwuid_r(uid_t, struct passwd *, char *, size_t, struct passwd **);
int getpwnam_r(const char *, struct passwd *, char *, size_t, struct passwd **);
struct passwd *getpwent(void);
void setpwent(void);
void endpwent(void);
typedef __darwin_uuid_t uuid_t;
typedef __darwin_uuid_string_t uuid_string_t;
void uuid_clear(uuid_t uu);
int uuid_compare(const uuid_t uu1, const uuid_t uu2);
void uuid_copy(uuid_t dst, const uuid_t src);
void uuid_generate(uuid_t out);
void uuid_generate_random(uuid_t out);
void uuid_generate_time(uuid_t out);
int uuid_is_null(const uuid_t uu);
int uuid_parse(const uuid_string_t in, uuid_t uu);
void uuid_unparse(const uuid_t uu, uuid_string_t out);
void uuid_unparse_lower(const uuid_t uu, uuid_string_t out);
void uuid_unparse_upper(const uuid_t uu, uuid_string_t out);
int setpassent(int);
char *user_from_uid(uid_t, int);
struct passwd *getpwuuid(uuid_t);
int getpwuuid_r(uuid_t, struct passwd *, char *, size_t, struct passwd **);
int pselect(int, fd_set * restrict, fd_set * restrict,
  fd_set * restrict, const struct timespec * restrict,
  const sigset_t * restrict);

  ;
struct accessx_descriptor {
 unsigned int ad_name_offset;
 int ad_flags;
 int ad_pad[2];
};
int getattrlistbulk(int, void *, void *, size_t, uint64_t) ;
int faccessat(int, const char *, int, int) ;
int fchownat(int, const char *, uid_t, gid_t, int) ;
int linkat(int, const char *, int, const char *, int) ;
ssize_t readlinkat(int, const char *, char *, size_t) ;
int symlinkat(const char *, int, const char *) ;
int unlinkat(int, const char *, int) ;
int getattrlistat(int, const char *, void *, void *, size_t, unsigned long) ;
void _exit(int) ;
int access(const char *, int);
unsigned int
  alarm(unsigned int);
int chdir(const char *);
int chown(const char *, uid_t, gid_t);
int close(int);
int dup(int);
int dup2(int, int);
int execl(const char *, const char *, ...);
int execle(const char *, const char *, ...);
int execlp(const char *, const char *, ...);
int execv(const char *, char * const *);
int execve(const char *, char * const *, char * const *);
int execvp(const char *, char * const *);
pid_t fork(void);
long fpathconf(int, int);
char *getcwd(char *, size_t);
gid_t getegid(void);
uid_t geteuid(void);
gid_t getgid(void);
int getgroups(int, gid_t []);
char *getlogin(void);
pid_t getpgrp(void);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
int isatty(int);
int link(const char *, const char *);
off_t lseek(int, off_t, int);
long pathconf(const char *, int);
int pause(void);
int pipe(int [2]);
ssize_t read(int, void *, size_t);
int rmdir(const char *);
int setgid(gid_t);
int setpgid(pid_t, pid_t);
pid_t setsid(void);
int setuid(uid_t);
unsigned int
  sleep(unsigned int);
long sysconf(int);
pid_t tcgetpgrp(int);
int tcsetpgrp(int, pid_t);
char *ttyname(int);
int ttyname_r(int, char *, size_t);
int unlink(const char *);
ssize_t write(int, const void *, size_t);
size_t confstr(int, char *, size_t);
int getopt(int, char * const [], const char *);
extern char *optarg;
extern int optind, opterr, optopt;
void *brk(const void *);
int chroot(const char *) ;
char *crypt(const char *, const char *);
void encrypt(char *, int);
int fchdir(int);
long gethostid(void);
pid_t getpgid(pid_t);
pid_t getsid(pid_t);
int getdtablesize(void) ;
int getpagesize(void) ;
char *getpass(const char *) ;
char *getwd(char *) ;
int lchown(const char *, uid_t, gid_t);
int lockf(int, int, off_t);
int nice(int);
ssize_t pread(int, void *, size_t, off_t);
ssize_t pwrite(int, const void *, size_t, off_t);
void *sbrk(int);
pid_t setpgrp(void);
int setregid(gid_t, gid_t);
int setreuid(uid_t, uid_t);
void swab(const void * restrict, void * restrict, ssize_t);
void sync(void);
int truncate(const char *, off_t);
useconds_t ualarm(useconds_t, useconds_t);
int usleep(useconds_t);
pid_t vfork(void);
int fsync(int);
int ftruncate(int, off_t);
int getlogin_r(char *, size_t);
int fchown(int, uid_t, gid_t);
int gethostname(char *, size_t);
ssize_t readlink(const char * restrict, char * restrict, size_t);
int setegid(gid_t);
int seteuid(uid_t);
int symlink(const char *, const char *);
void _Exit(int) ;
int accessx_np(const struct accessx_descriptor *, size_t, int *, uid_t);
int acct(const char *);
int add_profil(char *, size_t, unsigned long, unsigned int);
void endusershell(void);
int execvP(const char *, const char *, char * const *);
char *fflagstostr(unsigned long);
int getdomainname(char *, int);
int getgrouplist(const char *, int, int *, int *);
int gethostuuid(uuid_t, const struct timespec *) ;
mode_t getmode(const void *, mode_t);
int getpeereid(int, uid_t *, gid_t *);
int getsgroups_np(int *, uuid_t);
char *getusershell(void);
int getwgroups_np(int *, uuid_t);
int initgroups(const char *, int);
int iruserok(unsigned long, int, const char *, const char *);
int iruserok_sa(const void *, int, int, const char *, const char *);
int issetugid(void);
char *mkdtemp(char *);
int mknod(const char *, mode_t, dev_t);
int mkpath_np(const char *path, mode_t omode) ;
int mkstemp(char *);
int mkstemps(char *, int);
char *mktemp(char *);
int nfssvc(int, void *);
int profil(char *, size_t, unsigned long, unsigned int);
int pthread_setugid_np(uid_t, gid_t);
int pthread_getugid_np( uid_t *, gid_t *);
int rcmd(char **, int, const char *, const char *, const char *, int *);
int rcmd_af(char **, int, const char *, const char *, const char *, int *,
  int);
int reboot(int);
int revoke(const char *);
int rresvport(int *);
int rresvport_af(int *, int);
int ruserok(const char *, int, const char *, const char *);
int setdomainname(const char *, int);
int setgroups(int, const gid_t *);
void sethostid(long);
int sethostname(const char *, int);
void setkey(const char *);
int setlogin(const char *);
void *setmode(const char *);
int setrgid(gid_t);
int setruid(uid_t);
int setsgroups_np(int, const uuid_t);
void setusershell(void);
int setwgroups_np(int, const uuid_t);
int strtofflags(char **, unsigned long *, unsigned long *);
int swapon(const char *);
int syscall(int, ...);
int ttyslot(void);
int undelete(const char *);
int unwhiteout(const char *);
void *valloc(size_t);
extern char *suboptarg;
int getsubopt(char **, char * const *, char **);
int fgetattrlist(int,void*,void*,size_t,unsigned int) ;
int fsetattrlist(int,void*,void*,size_t,unsigned int) ;
int getattrlist(const char*,void*,void*,size_t,unsigned int);
int setattrlist(const char*,void*,void*,size_t,unsigned int);
int exchangedata(const char*,const char*,unsigned int);
int getdirentriesattr(int,void*,void*,size_t,unsigned int*,unsigned int*,unsigned int*,unsigned int);
struct fssearchblock;
struct searchstate;
int searchfs(const char *, struct fssearchblock *, unsigned long *, unsigned int, unsigned int, struct searchstate *);
int fsctl(const char *,unsigned long,void*,unsigned int);
int ffsctl(int,unsigned long,void*,unsigned int) ;
int fsync_volume_np(int, int) ;
int sync_volume_np(const char *, int) ;
extern int optreset;
struct dirent;
struct stat;
typedef struct {
 size_t gl_pathc;
 int gl_matchc;
 size_t gl_offs;
 int gl_flags;
 char **gl_pathv;
 union {
  int (*gl_errfunc)(const char *, int);
 };
 void (*gl_closedir)(void *);
 struct dirent *(*gl_readdir)(void *);
 void *(*gl_opendir)(const char *);
 int (*gl_lstat)(const char *, struct stat *);
 int (*gl_stat)(const char *, struct stat *);
} glob_t;
int glob(const char * restrict, int, int (*)(const char *, int),
      glob_t * restrict);
void globfree(glob_t *);
typedef __darwin_off_t regoff_t;
typedef struct {
 int re_magic;
 size_t re_nsub;
 const char *re_endp;
 struct re_guts *re_g;
} regex_t;
typedef struct {
 regoff_t rm_so;
 regoff_t rm_eo;
} regmatch_t;
int regcomp(regex_t * restrict, const char * restrict, int);
size_t regerror(int, const regex_t * restrict, char * restrict, size_t);
int regexec(const regex_t * restrict, const char * restrict, size_t,
     regmatch_t __pmatch[], int);
void regfree(regex_t *);
int regncomp(regex_t * restrict, const char * restrict, size_t, int);
     ;
int regnexec(const regex_t * restrict, const char * restrict, size_t,
     size_t, regmatch_t __pmatch[], int);
     ;
int regwcomp(regex_t * restrict, const wchar_t * restrict, int);
     ;
int regwexec(const regex_t * restrict, const wchar_t * restrict, size_t,
     regmatch_t __pmatch[], int);
     ;
int regwncomp(regex_t * restrict, const wchar_t * restrict, size_t, int);
     ;
int regwnexec(const regex_t * restrict, const wchar_t * restrict,
     size_t, size_t, regmatch_t __pmatch[], int);
     ;
struct __semid_ds_new
{
 struct ipc_perm sem_perm;
 __int32_t sem_base;
 unsigned short sem_nsems;
 time_t sem_otime;
 __int32_t sem_pad1;
 time_t sem_ctime;
 __int32_t sem_pad2;
 __int32_t sem_pad3[4];
};
struct sem {
 unsigned short semval;
 pid_t sempid;
 unsigned short semncnt;
 unsigned short semzcnt;
};
struct sembuf {
 unsigned short sem_num;
 short sem_op;
 short sem_flg;
};
union semun {
 int val;
 struct __semid_ds_new *buf;
 unsigned short *array;
};
typedef union semun semun_t;
int semsys(int, ...);
int semctl(int, int, int, ...);
int semget(key_t, int, int);
int semop(int, struct sembuf *, size_t);
struct utimbuf {
 time_t actime;
 time_t modtime;
};
int utime(const char *, const struct utimbuf *);
struct group {
 char *gr_name;
 char *gr_passwd;
 gid_t gr_gid;
 char **gr_mem;
};
struct group *getgrgid(gid_t);
struct group *getgrnam(const char *);
int getgrgid_r(gid_t, struct group *, char *, size_t, struct group **);
int getgrnam_r(const char *, struct group *, char *, size_t, struct group **);
struct group *getgrent(void);
void setgrent(void);
void endgrent(void);
char *group_from_gid(gid_t, int);
struct group *getgruuid(uuid_t);
int getgruuid_r(uuid_t, struct group *, char *, size_t, struct group **);
void setgrfile(const char *);
int setgroupent(int);
typedef unsigned short shmatt_t;
struct __shmid_ds_new
{
 struct ipc_perm shm_perm;
 size_t shm_segsz;
 pid_t shm_lpid;
 pid_t shm_cpid;
 shmatt_t shm_nattch;
 time_t shm_atime;
 time_t shm_dtime;
 time_t shm_ctime;
 void *shm_internal;
};
int shmsys(int, ...);
void *shmat (int, const void *, int);
int shmctl(int, int, struct __shmid_ds_new *);
int shmdt(const void *);
int shmget(key_t, size_t, int);
struct utmpx {
 char ut_user[256];
 char ut_id[4];
 char ut_line[32];
 pid_t ut_pid;
 short ut_type;
 struct timeval ut_tv;
 char ut_host[256];
 __uint32_t ut_pad[16];
};
struct lastlogx {
 struct timeval ll_tv;
 char ll_line[32];
 char ll_host[256];
};
void endutxent(void);
void endutxent_wtmp(void) ;
struct lastlogx *
 getlastlogx(uid_t, struct lastlogx *) ;
struct lastlogx *
 getlastlogxbyname(const char*, struct lastlogx *);
struct utmp;
void getutmp(const struct utmpx *, struct utmp *) ;
void getutmpx(const struct utmp *, struct utmpx *) ;
struct utmpx *
 getutxent(void);
struct utmpx *
 getutxent_wtmp(void) ;
struct utmpx *
 getutxid(const struct utmpx *);
struct utmpx *
 getutxline(const struct utmpx *);
struct utmpx *
 pututxline(const struct utmpx *);
void setutxent(void);
void setutxent_wtmp(int) ;
int utmpxname(const char *) ;
int wtmpxname(const char *) ;
extern int _libiconv_version;
typedef void* iconv_t;
iconv_t iconv_open (const char* , const char* );
size_t iconv (iconv_t ,
 char ** restrict , size_t * restrict ,
 char ** restrict , size_t * restrict );
int iconv_close (iconv_t );
int iconvctl (iconv_t , int , void* );
typedef void (*iconv_unicode_char_hook) (unsigned int uc, void* data);
typedef void (*iconv_wide_char_hook) (wchar_t wc, void* data);
struct iconv_hooks {
  iconv_unicode_char_hook uc_hook;
  iconv_wide_char_hook wc_hook;
  void* data;
};
void iconvlist (int (* ) (unsigned int ,
                                      const char * const * ,
                                      void* ),
                       void* );
extern const char * iconv_canonicalize (const char * name);
void libiconv_set_relocation_prefix (const char * ,
         const char * );
typedef struct entry {
 char *key;
 void *data;
} ENTRY;
typedef enum {
 FIND, ENTER
} ACTION;
typedef enum {
 preorder,
 postorder,
 endorder,
 leaf
} VISIT;
int hcreate(size_t);
void hdestroy(void);
ENTRY *hsearch(ENTRY, ACTION);
void insque(void *, void *);
void *lfind(const void *, const void *, size_t *, size_t,
     int (*)(const void *, const void *));
void *lsearch(const void *, void *, size_t *, size_t,
     int (*)(const void *, const void *));
void remque(void *);
void *tdelete(const void * restrict, void ** restrict,
     int (*)(const void *, const void *));
void *tfind(const void *, void * const *,
     int (*)(const void *, const void *));
void *tsearch(const void *, void **, int (*)(const void *, const void *));
void twalk(const void *, void (*)(const void *, VISIT, int));
typedef __darwin_mbstate_t mbstate_t;
typedef __darwin_wctype_t wctype_t;
wctype_t
 wctype(const char *);
wint_t btowc(int);
wint_t fgetwc(FILE *);
wchar_t *fgetws(wchar_t * restrict, int, FILE * restrict);
wint_t fputwc(wchar_t, FILE *);
int fputws(const wchar_t * restrict, FILE * restrict);
int fwide(FILE *, int);
int fwprintf(FILE * restrict, const wchar_t * restrict, ...);
int fwscanf(FILE * restrict, const wchar_t * restrict, ...);
wint_t getwc(FILE *);
wint_t getwchar(void);
size_t mbrlen(const char * restrict, size_t, mbstate_t * restrict);
size_t mbrtowc(wchar_t * restrict, const char * restrict, size_t,
     mbstate_t * restrict);
int mbsinit(const mbstate_t *);
size_t mbsrtowcs(wchar_t * restrict, const char ** restrict, size_t,
     mbstate_t * restrict);
wint_t putwc(wchar_t, FILE *);
wint_t putwchar(wchar_t);
int swprintf(wchar_t * restrict, size_t, const wchar_t * restrict, ...);
int swscanf(const wchar_t * restrict, const wchar_t * restrict, ...);
wint_t ungetwc(wint_t, FILE *);
int vfwprintf(FILE * restrict, const wchar_t * restrict,
     __darwin_va_list);
int vswprintf(wchar_t * restrict, size_t, const wchar_t * restrict,
     __darwin_va_list);
int vwprintf(const wchar_t * restrict, __darwin_va_list);
size_t wcrtomb(char * restrict, wchar_t, mbstate_t * restrict);
wchar_t *wcscat(wchar_t * restrict, const wchar_t * restrict);
wchar_t *wcschr(const wchar_t *, wchar_t);
int wcscmp(const wchar_t *, const wchar_t *);
int wcscoll(const wchar_t *, const wchar_t *);
wchar_t *wcscpy(wchar_t * restrict, const wchar_t * restrict);
size_t wcscspn(const wchar_t *, const wchar_t *);
size_t wcsftime(wchar_t * restrict, size_t, const wchar_t * restrict,
     const struct tm * restrict);
size_t wcslen(const wchar_t *);
wchar_t *wcsncat(wchar_t * restrict, const wchar_t * restrict, size_t);
int wcsncmp(const wchar_t *, const wchar_t *, size_t);
wchar_t *wcsncpy(wchar_t * restrict , const wchar_t * restrict, size_t);
wchar_t *wcspbrk(const wchar_t *, const wchar_t *);
wchar_t *wcsrchr(const wchar_t *, wchar_t);
size_t wcsrtombs(char * restrict, const wchar_t ** restrict, size_t,
     mbstate_t * restrict);
size_t wcsspn(const wchar_t *, const wchar_t *);
wchar_t *wcsstr(const wchar_t * restrict, const wchar_t * restrict);
size_t wcsxfrm(wchar_t * restrict, const wchar_t * restrict, size_t);
int wctob(wint_t);
double wcstod(const wchar_t * restrict, wchar_t ** restrict);
wchar_t *wcstok(wchar_t * restrict, const wchar_t * restrict,
     wchar_t ** restrict);
long wcstol(const wchar_t * restrict, wchar_t ** restrict, int);
unsigned long
  wcstoul(const wchar_t * restrict, wchar_t ** restrict, int);
wchar_t *wmemchr(const wchar_t *, wchar_t, size_t);
int wmemcmp(const wchar_t *, const wchar_t *, size_t);
wchar_t *wmemcpy(wchar_t * restrict, const wchar_t * restrict, size_t);
wchar_t *wmemmove(wchar_t *, const wchar_t *, size_t);
wchar_t *wmemset(wchar_t *, wchar_t, size_t);
int wprintf(const wchar_t * restrict, ...);
int wscanf(const wchar_t * restrict, ...);
int wcswidth(const wchar_t *, size_t);
int wcwidth(wchar_t);
int vfwscanf(FILE * restrict, const wchar_t * restrict,
     __darwin_va_list);
int vswscanf(const wchar_t * restrict, const wchar_t * restrict,
     __darwin_va_list);
int vwscanf(const wchar_t * restrict, __darwin_va_list);
float wcstof(const wchar_t * restrict, wchar_t ** restrict);
long double
 wcstold(const wchar_t * restrict, wchar_t ** restrict);
long long
 wcstoll(const wchar_t * restrict, wchar_t ** restrict, int);
unsigned long long
 wcstoull(const wchar_t * restrict, wchar_t ** restrict, int);
size_t mbsnrtowcs(wchar_t * restrict, const char ** restrict, size_t,
            size_t, mbstate_t * restrict);
wchar_t *wcpcpy(wchar_t * restrict, const wchar_t * restrict) ;
wchar_t *wcpncpy(wchar_t * restrict, const wchar_t * restrict, size_t) ;
wchar_t *wcsdup(const wchar_t *) ;
int wcscasecmp(const wchar_t *, const wchar_t *) ;
int wcsncasecmp(const wchar_t *, const wchar_t *, size_t n) ;
size_t wcsnlen(const wchar_t *, size_t) ;
size_t wcsnrtombs(char * restrict, const wchar_t ** restrict, size_t,
            size_t, mbstate_t * restrict);
wchar_t *fgetwln(FILE * restrict, size_t *) ;
size_t wcslcat(wchar_t *, const wchar_t *, size_t);
size_t wcslcpy(wchar_t *, const wchar_t *, size_t);

extern intmax_t
imaxabs(intmax_t j);
typedef struct {
 intmax_t quot;
 intmax_t rem;
} imaxdiv_t;

extern imaxdiv_t
imaxdiv(intmax_t __numer, intmax_t __denom);

extern intmax_t
strtoimax(const char * restrict __nptr,
   char ** restrict __endptr,
   int __base);

extern uintmax_t
strtoumax(const char * restrict __nptr,
   char ** restrict __endptr,
   int __base);

extern intmax_t
wcstoimax(const wchar_t * restrict __nptr,
   wchar_t ** restrict __endptr,
   int __base);

extern uintmax_t
wcstoumax(const wchar_t * restrict __nptr,
   wchar_t ** restrict __endptr,
   int __base);
typedef int sem_t;
int sem_close(sem_t *);
int sem_destroy(sem_t *) ;
int sem_getvalue(sem_t * restrict, int * restrict) ;
int sem_init(sem_t *, int, unsigned int) ;
sem_t * sem_open(const char *, int, ...);
int sem_post(sem_t *);
int sem_trywait(sem_t *);
int sem_unlink(const char *);
int sem_wait(sem_t *);
typedef __darwin_wctrans_t wctrans_t;
wint_t nextwctype(wint_t, wctype_t);
wint_t towctrans(wint_t, wctrans_t);
wctrans_t
 wctrans(const char *);
typedef int jmp_buf[((9 * 2) + 3 + 16)];
typedef int sigjmp_buf[((9 * 2) + 3 + 16) + 1];
extern int setjmp(jmp_buf);
extern void longjmp(jmp_buf, int) ;
int _setjmp(jmp_buf);
void _longjmp(jmp_buf, int) ;
int sigsetjmp(sigjmp_buf, int);
void siglongjmp(sigjmp_buf, int) ;
void longjmperror(void);
struct statvfs {
 unsigned long f_bsize;
 unsigned long f_frsize;
 fsblkcnt_t f_blocks;
 fsblkcnt_t f_bfree;
 fsblkcnt_t f_bavail;
 fsfilcnt_t f_files;
 fsfilcnt_t f_ffree;
 fsfilcnt_t f_favail;
 unsigned long f_fsid;
 unsigned long f_flag;
 unsigned long f_namemax;
};
int fstatvfs(int, struct statvfs *);
int statvfs(const char * restrict, struct statvfs * restrict);
typedef struct {
 size_t we_wordc;
 char **we_wordv;
 size_t we_offs;
} wordexp_t;
int wordexp(const char * restrict, wordexp_t * restrict, int) ;
void wordfree(wordexp_t *) ;
char *nl_langinfo(nl_item);
extern const char *const sys_signame[32];
extern const char *const sys_siglist[32];
int raise(int);
void (*bsd_signal(int, void (*)(int)))(int);
int kill(pid_t, int);
int killpg(pid_t, int);
int pthread_kill(pthread_t, int);
int pthread_sigmask(int, const sigset_t *, sigset_t *);
int sigaction(int, const struct sigaction * restrict,
     struct sigaction * restrict);
int sigaddset(sigset_t *, int);
int sigaltstack(const stack_t * restrict, stack_t * restrict);
int sigdelset(sigset_t *, int);
int sigemptyset(sigset_t *);
int sigfillset(sigset_t *);
int sighold(int);
int sigignore(int);
int siginterrupt(int, int);
int sigismember(const sigset_t *, int);
int sigpause(int);
int sigpending(sigset_t *);
int sigprocmask(int, const sigset_t * restrict, sigset_t * restrict);
int sigrelse(int);
void (*sigset(int, void (*)(int)))(int);
int sigsuspend(const sigset_t *);
int sigwait(const sigset_t * restrict, int * restrict);
void psignal(unsigned int, const char *);
int sigblock(int);
int sigsetmask(int);
int sigvec(int, struct sigvec *, struct sigvec *);
