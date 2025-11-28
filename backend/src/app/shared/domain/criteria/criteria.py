""""Domain criteria for patient registration."""

from typing import Literal


Operator = Literal[
    "EQUAL",
    "NOT_EQUAL",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL",
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL"
]


class Filter:
    """Filter class to handle query parameters for patient registration."""

    def __init__(self, field: str, operator: str, value: any):
        self.field = field
        self.operator = operator
        self.value = value

    def get_operator_sql(self) -> str:
        """Get SQL operator from filter operator."""
        operator_mapping = {
            "EQUAL": "=",
            "NOT_EQUAL": "!=",
            "LESS_THAN": "<",
            "LESS_THAN_OR_EQUAL": "<=",
            "GREATER_THAN": ">",
            "GREATER_THAN_OR_EQUAL": ">="
        }
        return operator_mapping.get(self.operator, "=")


OrderDirection = Literal["ASC", "DESC"]


class Order:
    """Order class to handle query parameters for patient registration."""

    def __init__(self, field: str, direction: OrderDirection):
        self.field = field
        self.direction: OrderDirection = direction


class Pagination:
    """Pagination class to handle query parameters for patient registration."""

    def __init__(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page


class Criteria:
    """Criteria class to handle query parameters for patient registration."""

    def __init__(self):
        self.filters: list[Filter] = []
        self.orders: Order = None
        self.pagination: Pagination = None

    def add_filter(self, filter: Filter) -> None:
        """Add filter to criteria."""
        self.filters.append(filter)

    def set_orders(self, orders: Order) -> None:
        """Set orders to criteria."""
        self.orders = orders

    def set_pagination(self, pagination: Pagination) -> None:
        """Set pagination to criteria."""
        self.pagination = pagination

    def to_dict(self) -> dict[str, any]:
        """Convert criteria to dictionary."""
        return {
            "filters": [filter.__dict__ for filter in self.filters],
            "orders": self.orders.__dict__ if self.orders else None,
            "pagination": self.pagination.__dict__ if self.pagination else None
        }


class CriteriaParser:
    """Criteria class to handle query parameters for patient registration."""

    def dict_to_criteria(self, query_params:  dict[str, any]) -> Criteria:
        """Convert dictionary to criteria attributes."""

        criteria = Criteria()

        print(f"query_params {query_params}")

        # get data for ordering
        order_by_key = "orderBy"
        order_dir_key = "order"
        if order_by_key in query_params and order_dir_key in query_params:
            order = Order(
                field=query_params[order_by_key],
                direction=query_params[order_dir_key]
            )
            print(f"order {order.__dict__}")
            criteria.set_orders(order)

        # Parse filters from query_params
        # full_name, contact
        max_filters = 2
        i = 0
        while i < max_filters:
            field_key = f"{i}_field"
            operator_key = f"{i}_operator"
            value_key = f"{i}_value"
            if field_key in query_params and operator_key in query_params and value_key in query_params:
                filter_obj = Filter(
                    field=query_params[field_key],
                    operator=query_params[operator_key],
                    value=query_params[value_key]
                )
                print(f"filter_obj {filter_obj.__dict__}")
                criteria.add_filter(filter_obj)
                # # Remove used keys
                # query_params.pop(field_key, None)
                # query_params.pop(operator_key, None)
                # query_params.pop(value_key, None)
                i += 1
            else:
                i += 1
                continue

        # Parse pagination from query_params
        try:

            # keys
            page_key = "page"
            per_page_key = "per_page"

            # values
            page_value = 1
            per_page_value = 10

            if page_key in query_params and query_params[page_key].isdigit():
                value_aux = int(query_params[page_key])
                page_value = value_aux if value_aux > page_value else page_value

            if per_page_key in query_params and query_params[per_page_key].isdigit():
                value_aux = int(query_params[per_page_key])
                per_page_value = value_aux if value_aux > per_page_value else per_page_value

            pagination = Pagination(
                page=page_value,
                per_page=per_page_value
            )
            print(f"pagination {pagination.__dict__}")
            criteria.set_pagination(pagination)

            # # Remove used keys
            # query_params.pop(page_key, None)
            # query_params.pop(per_page_key, None)
        except RuntimeError:
            pass

        print(f"criteria {criteria.to_dict()}")

        return criteria
