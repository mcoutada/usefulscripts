import sqlparse

def set_lowercase_alias(query):
    # Parse the query into tokens
    parsed = sqlparse.parse(query)[0]
    
    for i in range(0, len(parsed.tokens)):
        token = parsed.tokens[i]
        
        # IdentifierList = columns or whatever is between SELECT and FROM
        if isinstance(token, sqlparse.sql.IdentifierList):
            identifiers_lst = list(token.get_identifiers())

            for j in range(0, len(token.tokens)):
                if token.tokens[j] in identifiers_lst:
                    identifier = token.tokens[j]
                    
                    # If the identifier has an alias, replace it with a lowercase version
                    if identifier.has_alias():
                        alias_token_str = identifier.get_alias()
                        
                        # Find the index of the alias token
                        for k in range(0, len(identifier.tokens)):
                            if identifier.tokens[k].value == alias_token_str:
                                identifier_alias_idx = k
                                break
                            
                        # Set the alias to lowercase double-quoted
                        alias_token_str = alias_token_str.lower()
                        if not(alias_token_str[0] == '"' and alias_token_str[-1] == '"'):
                            alias_token_str = f'"{alias_token_str}"'
                        alias_token = sqlparse.sql.Token(sqlparse.tokens.Name, alias_token_str)
                        identifier.tokens[identifier_alias_idx] = alias_token
                    
                    # If the identifier does not have an alias, add a lowercase version after the first token
                    else:
                        alias_token_str = f'"{identifier.token_first().value.lower()}"'
                        alias_token = sqlparse.sql.Token(sqlparse.tokens.Name, alias_token_str)
                        whitespace_token = sqlparse.sql.Token(sqlparse.tokens.Whitespace, " ")
                        identifier.insert_after(identifier.tokens[0], alias_token)
                        identifier.insert_after(identifier.tokens[0], whitespace_token)
        
    return str(parsed)

query = "SELECT Col1 Alias1, (SELECT COL2 Table2) AS Alias2, sum(col3) ALIAS3, COL4 FROM Table1 where COl1 = 1"
print(f'before:\n {query}')
query = set_lowercase_alias(query)

# Format the query with uppercase keywords, 4-space indentation, comma first, and spaces around operators
# query = sqlparse.format(query, reindent=True, keyword_case="upper", indent_width=4, comma_first=True, use_space_around_operators=True)

print(f'after:\n {query}')
