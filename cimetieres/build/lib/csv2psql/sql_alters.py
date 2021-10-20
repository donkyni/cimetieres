from textwrap import dedent
from os import popen
from sql_alter_strings import *
import logger

__author__ = 'Nicholas McCready'


def verify_dates(table_name, date_format, cols):
    not_nulls_str = " "
    for date in cols:
        not_nulls_str += date + " IS NOT NULL AND "
    # remove last AND
    not_nulls_str = not_nulls_str[:-4]

    return verify_dates_str.format(date_format=date_format,
                                   tablename=table_name,
                                   not_nulls=not_nulls_str)


def _join_keys(keys_to_join, join_char='_'):
    joined_str = ""
    i = 0
    length = len(keys_to_join)
    for key in keys_to_join:
        i += 1
        if not i == length:
            joined_str += key + " || '%s' || " % join_char
        else:
            joined_str += key
    return joined_str


def make_primary_key_w_join(tablename, primary_key_name, keys_to_join):
    deletion_str = bad_key_deletion_str.format(
        ors_missing_keys=_make_key_deletion_set(keys_to_join, primary_key_name),
        tablename=tablename)
    return join_keys_primary_str.format(
        tablename=tablename,
        primary_key=primary_key_name,
        keys_to_join=_join_keys(keys_to_join),
        maybe_force_deletion_on_bad_keys=deletion_str)


def dates(tablename, cols, dateformat):
    str = ""
    for col in cols:
        str += _date(tablename, col, dateformat) + "\n"
    return str


def _date(tablename, colname, dateformat):
    return date_str.format(tablename=tablename, col=colname, dateformat=dateformat, format_len=len(dateformat))


def _make_set(fieldnames, primary_key, temp_tablename, make_primary_first):
    str = ""
    array = _get_fieldnames_w_key(fieldnames, primary_key, make_primary_first)
    for key in array:
        if key != "SERIAL" and key != "TIMESTAMP":
            str += "{col} = {temp_table}.{col}".format(col=key, temp_table=temp_tablename) + ","

    return str[:-1]


def _make_key_deletion_set(fieldnames, primary_key):
    str = ""
    array = _get_fieldnames_w_key(fieldnames, primary_key, False)
    for key in array:
        if key != primary_key:
            str += "{col} IS NULL OR ".format(col=key)

    return str[:-4] + ";"


def delete_dupes(fieldnames, primary_key, temp_tablename, serial, debug=False):
    if debug:
        logger.debug(True, "-- delete dupes")

    obj = dupes_clause(fieldnames, primary_key, temp_tablename, serial)
    cols = ""
    specific_cols = ""

    obj['filtered_keys'].append(serial)
    # print obj['filtered_keys']
    for key in obj['filtered_keys']:
        cols += "%s, " % key
        specific_cols += "t1.%s, " % key
    cols = cols[:-2]
    specific_cols = specific_cols[:-2]

    this_select_str = select_dupes_str.format(
        tablename=temp_tablename,
        difference=obj['diff'],
        clause=obj['clause']
    )

    return delete_dups_str.format(
        tablename=temp_tablename,
        cols=cols,
        specific_cols=specific_cols,
        select_statement=this_select_str
    )


def fast_delete_dupes(fieldnames, primary_key, temp_tablename, debug=False):
    if debug:
        logger.debug(True, "-- delete dupes")

    obj = dupes_clause(fieldnames, primary_key, temp_tablename, '')
    specific_cols = ""

    for key in obj['filtered_keys']:
        specific_cols += "%s, " % key
    specific_cols = specific_cols[:-2]

    head, sep, tail = temp_tablename.partition(".")
    temp_tablename = tail
    return delete_dups_fast_str.format(
        tablename=temp_tablename,
        cols=specific_cols,
    )


def dupes_clause(fieldnames, primary_key, temp_tablename, serial):
    clause = ""
    array = _get_fieldnames_w_key(fieldnames, primary_key, False)
    keys = []
    for key in array:
        if key != primary_key:
            keys.append(key)
            clause += "AND t1.{col} = t2.{col}\n".format(col=key, tablename=temp_tablename)
    clause = clause[:-1]
    diff = "t1.{s} > t2.{s}".format(s=serial)

    return {'clause': clause, 'diff': diff, 'filtered_keys': keys}


def count_dupes(fieldnames, primary_key, temp_tablename, serial, debug=False):
    if debug:
        logger.debug(True, "-- count dupes")
    obj = dupes_clause(fieldnames, primary_key, temp_tablename, serial)
    return count_dups_str.format(
        tablename=temp_tablename,
        clause=obj['clause'],
        difference=obj['diff']
    )


def _get_fieldnames_w_key(fieldnames, primary_key, make_primary_first):
    # keep fieldnames immutable
    array = fieldnames[:]
    if make_primary_first:
        array.insert(0, primary_key)
    else:
        array.append(primary_key)
    return array


def _make_selects(fieldnames, primary_key, temp_tablename, make_primary_first, just_cols=False):
    str = ""
    array = _get_fieldnames_w_key(fieldnames, primary_key, make_primary_first)
    for col in array:
        if col != "SERIAL" and col != "TIMESTAMP":
            if just_cols:
                str += "{col}".format(col=col) + ","
            else:
                str += "{temp_table}.{col}".format(col=col, temp_table=temp_tablename) + ","
    return str[:-1]


def bulk_upsert(fieldnames, tablename, primary_key, make_primary_first, temp_tablename=None, new_tablename=None):
    if not temp_tablename:
        temp_tablename = "temp_" + tablename

    perm_tablename = new_tablename if new_tablename else tablename
    sets = _make_set(fieldnames, primary_key, temp_tablename, make_primary_first)
    selects = _make_selects(fieldnames, primary_key, temp_tablename, make_primary_first)
    cols = _make_selects(fieldnames, primary_key, temp_tablename, make_primary_first, True)

    ret = bulk_upsert_str.format(perm_table=perm_tablename,
                                 cols=cols,
                                 temp_table=temp_tablename,
                                 sets=sets,
                                 key=primary_key,
                                 selects=selects)
    return ret


def merge(fieldnames, tablename, primary_key, make_primary_first, temp_tablename, new_tablename=None, do_log=False):
    if do_log:
        logger.debug(True, "-- tablename: %s" % tablename)
        logger.debug(True, "-- fieldnames: %s" % fieldnames)
        logger.debug(True, "-- primary_key: %s" % primary_key)
        logger.debug(True, "-- temp_tablename: %s" % temp_tablename)

    return bulk_upsert(fieldnames, tablename, primary_key, make_primary_first, temp_tablename, new_tablename)


def pg_dump(db_name, schema_name, table_name, new_table_name=None, option="-s"):
    """
    see pg_dump_str

    This just executes pg_dump with popen and returns the output
    """
    cmd = pg_dump_str(db_name, schema_name, table_name, option)
    sql = popen(cmd).read()
    if new_table_name:
        pruned = table_name.split('.', 1)[-1]
        logger.info(True, "PRUNED tablename: %s" % pruned)
        sql = sql.replace(table_name.lower(), new_table_name)

    return sql


def add_col(name, type, tablename, additional=""):
    return add_col_str.format(
        tablename=tablename,
        col=name, type=type,
        additional=additional
    )


def add_cols(cols, tablename):
    str = ""
    for col in cols:
        str += add_col(col.name, col.type, tablename, col.additional)
    return str
