from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne import Application, rpc, Service, Unicode, error, AnyXml
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.complex import ComplexModel

from lixi_mock_valfirm_service.service.validators.valuation_message import authorized, valid_message


class AuthHeader(ComplexModel):
    __namespace__ = 'lixi.mock.valfirm.service'
    UserName = Unicode
    Password = Unicode


class MockValfirm(Service):
    __in_header__ = AuthHeader

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Order(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Update(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Cancel(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def CancelAmend(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def AssignedValuer(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Delay(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def FeeChange(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def NoteAdded(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def QuoteRequest(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def QuoteResponse(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Error(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Amendment(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Escalate(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(AnyXml, _returns=Unicode,  _out_variable_name='result')
    def Complete(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)


schema = './files/ValuationTransaction_1_6.xsd'


def validate_message(username, password, valuation_message):
    try:
        if not authorized(username, password):
            raise error.Fault(
                faultcode='Client', faultstring='Unable to process request. UserName or Password is incorrect.')
    except ValueError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. No authorisation provided.')

    try:
        if not valid_message(valuation_message, schema):
            raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')
    except AttributeError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')

    return "0"


application = Application([MockValfirm], 'lixi.mock.valfirm.service',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

mock_valfirm_service = csrf_exempt(DjangoApplication(application))