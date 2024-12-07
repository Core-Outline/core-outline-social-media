import operator
queries_table = 'query'

query_actions = {
    'less_than': operator.lt,
    'greater_than': operator.gt,
    # 'in': operator.,
    'greater_than_equal_to': operator.ge,
    'less_than_equal_to': operator.le,
}
