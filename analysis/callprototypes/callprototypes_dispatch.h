typedef void * id;
typedef long dispatch_once_t;
typedef void * dispatch_block_t;

void dispatch_once(dispatch_once_t *predicate, dispatch_block_t block);
