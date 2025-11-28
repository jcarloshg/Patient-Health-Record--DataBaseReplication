"""Convert Criteria object to SQL query string."""

from src.app.shared.domain.criteria.criteria import Criteria


class CriteriaToSQL:
    """Convert Criteria object to SQL query string."""

    def __init__(self):
        self.table_name: str = ""
        self.where_clause: list = []
        self.params: dict = {}
        self.order_clause: str = ""
        self.pagination_clause: str = ""

    def set_table_name(self, table_name: str) -> None:
        """Set the table name for SQL queries."""
        self.table_name = table_name

    def set_where_by_criteria(self, criteria: Criteria) -> None:
        """Set WHERE clause based on Criteria filters."""

        # Convert filters to SQL WHERE clause
        if not criteria.filters:
            return

        filter_clauses = []
        index = 1
        for flt in criteria.filters:
            clause = f"{flt.field} {flt.get_operator_sql()} :where_param_{index}"
            filter_clauses.append(clause)
            self.params[f"where_param_{index}"] = flt.value
            index += 1
        self.where_clause = filter_clauses

    def set_order_by_criteria(self, criteria: Criteria) -> None:
        """Set ORDER BY clause based on Criteria orders."""
        if not criteria.orders:
            return

        order_clause = f"ORDER BY {criteria.orders.field} {criteria.orders.direction}"
        self.order_clause = order_clause

    def set_pagination_by_criteria(self, criteria: Criteria) -> None:
        """Set pagination based on Criteria pagination."""
        if not criteria.pagination:
            return

        limit = criteria.pagination.per_page
        offset = (criteria.pagination.page - 1) * criteria.pagination.per_page
        pagination_clause = f"LIMIT {limit} OFFSET {offset}"
        self.pagination_clause = pagination_clause

    def get_select_query_parametrized(self) -> tuple[str, dict]:
        """Get the full SQL query string and parameters."""
        query = f"SELECT * FROM {self.table_name}"

        if self.where_clause:
            where_statement = " AND ".join(self.where_clause)
            query += f" WHERE {where_statement}"

        if self.order_clause:
            query += f" {self.order_clause}"

        if self.pagination_clause:
            query += f" {self.pagination_clause}"

        return query, self.params
