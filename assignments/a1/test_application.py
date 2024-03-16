from application import process_event_history
from customer import Customer
def test_app() -> None:
    log = {'events':[{"type": "call",
                      "src_number": "422-4785",
                      "dst_number": "136-5226",
                      "time": "2018-01-03 02:14:31",
                      "duration": 117,
                      "src_loc": [-79.68079993411648, 43.64986163420895],
                      "dst_loc": [-79.46762523704258, 43.59568659654661]}]}
    assert process_event_history(log, [Customer(1111)])
