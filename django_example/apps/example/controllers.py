from django_ignitor import BaseController
from apps.example.models import Account
from libs.shared import telapi_account

class IndexController(BaseController):
    def indexAction(self, request):
        pass

class AccountController(BaseController):
    # Maps to /account/forgot-password
    def forgotPasswordAction(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if len(username):
                try:
                    account = Account.objects.get(username=username)
                    
                    if account.phone_number:
                        sms_message = telapi_account.sms_messages.create(
                            from_number = settings.TELAPI_DID,
                            to_number   = account.phone_number,
                            body        = 'Your password is : %s' % account.password
                        )
                        
                        return self.redirect('/account/password-sent')
                    else:
                        self.template_dict['error'] = 'You do not have a phone number on file, uh oh!'
                except Account.DoesNotExist, e:
                    self.template_dict['error'] = 'Invalid username provided!'
            else:
                self.template_dict['error'] = 'Invalid username provided!'
    
    # Maps to /account/home
    def homeAction(self, request):
        if 'account_id' not in request.session:
            return self.redirect('/account/log-in')
        
        self.template_dict['account'] = Account.objects.get(id=request.session['account_id'])
    
    # Maps to /account/log-in
    def logInAction(self, request):
        if request.method == 'POST':
            username = request.POST.get('username') or ''
            password = request.POST.get('password') or ''
            
            if len(username) and len(password):
                try:
                    account = Account.objects.get(username=username, password=password)
                    
                    request.session['account_id'] = account.id
                    
                    return self.redirect('/account/home')
                    
                except Account.DoesNotExist, e:
                    self.template_dict['error'] = 'Invalid username / password provided!'
                    
            elif not len(username):
                self.template_dict['error'] = 'No username provided!'
                
            elif not len(password):
                self.template_dict['error'] = 'No password provided!'
    
    def logOutAction(self, request):
        request.session.clear()
        
        return self.redirect('/account/log-in')
    
    # Maps to /account/password-sent
    def passwordSentAction(self, request):
        # You can still return things here, and the controller will use it!
        return self.render_to_response('account/password-sent.html')

class RouteExampleController(BaseController):
    """Manipulate Default Routes
    
    This controller shows how easy it is to manipulate the default
    route provided for all of the actions, assigning usable variables
    to each action defined.
    """
    class Meta:
        route = r'^:controller/:action/(?P<random_id>\d+)$'
    
    def indexAction(self, request, random_id):
        return self.respond('Index Action : %s' % random_id)
        
    def testAction(self, request, random_id):
        return self.respond('Test Action : %s' % random_id)