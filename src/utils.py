from collections import namedtuple


def parse_data(data) -> namedtuple:
    Result = namedtuple('Result', 'order user partner contractor room')
    order_id = data['id']
    user_id = data['userId']
    contractor_id = data.get('contractorId') or user_id
    partner_id = data.get('partnerId') or user_id
    if not order_id or not contractor_id:
        raise ValueError('Bad request')
    return Result(order_id, user_id, partner_id, contractor_id, f"{order_id}_{contractor_id}")


def get_filters(result):
    filters = {
        'contractor_id': result.contractor,
        'order_id': result.order,
    }
    if result.user != result.contractor:
        filters['partner_id'] = result.user
    return filters
