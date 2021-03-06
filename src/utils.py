from collections import namedtuple

ParseResult = namedtuple('ParseResult', 'order user partner contractor room page page_size')
NamedUser = namedtuple('NamedUser', 'full_name avatar')


def parse_data(data) -> ParseResult:
    order_id = data['id']
    user_id = data['userId']
    contractor_id = data.get('contractorId') or user_id
    partner_id = data.get('partnerId') or user_id

    page = data.get('page')
    page_size = data.get('page_size', 10)

    if not order_id or not contractor_id:
        raise ValueError('Bad request')
    return ParseResult(
        order_id, user_id, partner_id, contractor_id, f"{order_id}_{contractor_id}", page, page_size,
    )


def get_filters(result):
    filters = {
        'contractor_id': result.contractor,
        'order_id': result.order,
    }
    if result.user != result.contractor:
        filters['partner_id'] = result.user
    return filters


def validate_fields(data, fields):
    for field in fields:
        if field not in data:
            return False
    return True
