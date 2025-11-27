"""Convert Criteria object to SQL query string."""

from src.app.shared.domain.criteria.criteria import Criteria


class CriteriaToSQL:
    """Convert Criteria object to SQL query string."""

    def criteria_to_sql(self, criteria: Criteria) -> str:
        """Convert Criteria object to SQL query string."""
        sql_parts = []

        # Convert filters to SQL WHERE clause
        if criteria.filters:
            filter_clauses = []
            for filter in criteria.filters:
                clause = f"{filter.field} {filter.operator} '{filter.value}'"
                filter_clauses.append(clause)
            where_clause = " AND ".join(filter_clauses)
            sql_parts.append(f"WHERE {where_clause}")

        # Convert orders to SQL ORDER BY clause
        if criteria.orders:
            order_clause = f"ORDER BY {criteria.orders.field} {criteria.orders.direction}"
            sql_parts.append(order_clause)

        # Convert pagination to SQL LIMIT and OFFSET clause
        if criteria.pagination:
            limit = criteria.pagination.per_page
            offset = (criteria.pagination.page - 1) * \
                criteria.pagination.per_page
            pagination_clause = f"LIMIT {limit} OFFSET {offset}"
            sql_parts.append(pagination_clause)

        # Combine all parts into a single SQL query string
        sql_query = " ".join(sql_parts)
        return sql_query

    def criteria_to_sql_parametrized(self, criteria: Criteria) -> tuple[str, list]:
        """
        Convert Criteria object to a parametrized SQL query string and parameters.

        Returns:
            tuple: (sql_query: str, params: list)
        """
        sql_parts = []
        params = []

        # Convert filters to SQL WHERE clause with parameters
        if criteria.filters:
            filter_clauses = []
            for filter in criteria.filters:
                clause = f"{filter.field} {filter.operator} %s"
                filter_clauses.append(clause)
                params.append(filter.value)
            where_clause = " AND ".join(filter_clauses)
            sql_parts.append(f"WHERE {where_clause}")

        # Convert orders to SQL ORDER BY clause
        if criteria.orders:
            order_clause = f"ORDER BY {criteria.orders.field} {criteria.orders.direction}"
            sql_parts.append(order_clause)

        # Convert pagination to SQL LIMIT and OFFSET clause
        if criteria.pagination:
            limit = criteria.pagination.per_page
            offset = (criteria.pagination.page - 1) * \
                criteria.pagination.per_page
            pagination_clause = f"LIMIT %s OFFSET %s"
            sql_parts.append(pagination_clause)
            params.extend([limit, offset])

        # Combine all parts into a single SQL query string
        sql_query = " ".join(sql_parts)
        return sql_query, params
