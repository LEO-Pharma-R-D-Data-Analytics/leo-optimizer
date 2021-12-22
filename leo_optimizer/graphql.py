import typing
import stringcase

from django.db.models import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import OneToOneRel
from django.db.models.query import QuerySet

from graphql.language.ast import FieldNode


def gql_optimizer(qs: QuerySet, top_node: FieldNode) -> QuerySet:
    """
    Function optimizes queryset base on model relations extracted from graphql query.

    :param QuerySet qs: QuerySet of a model to be optimized.
    :param FieldNode qs: Filed Node to be iterated.

    :return: QuerySet:
    """
    # Get select and prefetch related field paths.
    select_related, prefetch_related = extract_field_paths(top_node, qs.model)

    return qs.select_related(*select_related).prefetch_related(*prefetch_related)


def extract_field_paths(field_node: FieldNode, model: Model, prefix: str = '') -> typing.Tuple[typing.List[str], typing.List[str]]:
    """
    Optimizer fields on a query node.

    :param field_node: The field node containing the query to optimize.
    :param model: The model associated with the field node.
    :param prefix: The prefix to use for the fields.

    :return: The select and prefetch related field paths.
    """
    # The fields for the optimization.
    prefetch_fields = []
    selected_fields = []

    # Loop over sub-nodes of the FieldNode.
    for sub_node in field_node.selection_set.selections:
        # Only nodes with additional sub-nodes are relevant.
        if sub_node.selection_set:
            # Get field name.
            node_name = stringcase.snakecase(sub_node.name.value)

            # Check if the node is a model field.
            if hasattr(model, node_name):
                # Get model-field.
                field = model._meta.get_field(node_name)

                # Add one-to-N fields to select-fields
                if prefix == '' and isinstance(field, (OneToOneRel, ForeignKey)):
                    selected_fields.append(prefix + node_name)
                # Add many-to-N fields to prefetch-fields.
                else:
                    prefetch_fields.append(prefix + node_name)

                # Update prefix and model.
                new_prefix = prefix + node_name + '__'
                new_model = field.related_model
            else:
                # Use existing prefix and model.
                new_prefix = prefix
                new_model = model

            # Go deeper if node has additional node.
            nested_fields = extract_field_paths(sub_node, new_model, new_prefix)
            selected_fields += nested_fields[0]
            prefetch_fields += nested_fields[1]

    return selected_fields, prefetch_fields
