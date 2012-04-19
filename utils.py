from actandra import *

def sync_cassandra():
    sys = SystemManager()

    if KEYSPACE in sys.list_keyspaces():
        msg = 'Looks like you already have a %s keyspace.\n' % KEYSPACE
        msg += 'Do you want to delete it and recreate it?\n'
        msg += 'All current data will be deleted! (y/n): '
        resp = raw_input(msg)
        if not resp or resp[0] != 'y':
            print "Ok, then we're done here."
            return
        sys.drop_keyspace(KEYSPACE)

    sys.create_keyspace(KEYSPACE, SIMPLE_STRATEGY, {'replication_factor': '1'})
    sys.create_column_family(KEYSPACE, 'Subscribers', comparator_type=BYTES_TYPE)
    sys.create_column_family(KEYSPACE, 'Streams', comparator_type=LONG_TYPE)
    sys.create_column_family(KEYSPACE, 'Activities', comparator_type=BYTES_TYPE)
    sys.create_column_family(KEYSPACE, 'Comments', comparator_type=LONG_TYPE)
    sys.create_column_family(KEYSPACE, 'Likes', comparator_type=BYTES_TYPE)

    print 'All done!'

def truncate():
    SUBSCRIBERS.truncate()
    STREAMS.truncate()
    ACTIVITIES.truncate()
    COMMENTS.truncate()
    LIKES.truncate()