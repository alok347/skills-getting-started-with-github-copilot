def get_email_from_ldap(account_name, conn):
    """
    Fetches email for a given account name from the LDAP server.
    Implements retries for robustness.
    """
    search_filter = f"({LDAP_SEARCH_ATTRIBUTE}={account_name})"  # search filter for the LDAP query
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=[EMAIL_ATTRIBUTE],
                time_limit=LDAP_TIMEOUT
            )

            if conn.entries:
                return conn.entries[0][EMAIL_ATTRIBUTE].value
            else:
                return "Not Found"

        except LDAPException as e:
            logging.error(f"Attempt {attempt}: LDAP query failed for {account_name} - {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2)  # Wait before retrying
            else:
                return "LDAP Error"

        if not LDAP_PASSWORD or LDAP_PASSWORD.strip() == "":