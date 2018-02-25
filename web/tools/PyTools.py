def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size
 to human-readable form.


    Keyword arguments:

    size -- file size in bytes

    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024

                                if False, use multiples of 1000

    Returns: string

    '''

    SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],

                1024:
                    ['KiB',
                     'MiB',
                     'GiB',
                     'TiB',
                     'PiB',
                     'EiB',
                     'ZiB',
                     'YiB']}

    if size < 0:
        raise ValueError('numbermust be non-negative')

    if a_kilobyte_is_1024_bytes:
        multiple = 1024
    else:
        multiple = 1000

    for suffix in SUFFIXES[multiple]:
        size /= multiple

    if size < multiple:
        return '{0:.1f} {1}'.format(size, suffix)
    raise ValueError('number too large')
