from tastypie.resources import ModelResource
from tastypie import fields
from tarefas.models import Projeto, Tarefa, ProjetoUsuario
from django.contrib.auth.models import User
from tastypie.exceptions import NotFound
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.exceptions import Unauthorized

#            """ RESOURCE USUARIO """
class UsuarioResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get','post', 'delete','put']
        aways_return_data = True
        authorization = Authorization()
        filtering = {
            "Name": ('exact', 'startswith',)
        }

    def obj_create(self, bundle, **kwargs):
        print(bundle)
        if not(User.objects.filter(username = bundle.data['username'])):
            user = User()
            user.username = bundle.data['username']
            user.email = bundle.data['email']
            user.password = bundle.data['password']
            user.save()
            bundle.obj = user
            return bundle
        else:
            raise Unauthorized('Já existe Usuário com esse nome.')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized('Não permitido.')



#            """ RESOURCE PROJETO """
class ProjetoResource(ModelResource):
    class Meta:
        queryset = Projeto.objects.all()
        allowed_methods = ['get','post', 'delete','put']
        aways_return_data = True
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith',)
        }

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized('Não permitido.')

#            """ RESOURCE PROJETO_USUARIO """

class ProjetoUsuarioResource(ModelResource):
    class Meta:
        queryset = ProjetoUsuario.objects.all()
        allowed_methods = ['get','post', 'delete','put']
        aways_return_data = True
        authorization = Authorization()
        filtering = {
            "descricao": ('exact', 'startswith',)
        }
    def obj_create(self, bundle, **kwargs):
        usuario = bundle.data['usuario'].split("/")
        projeto = bundle.data['projeto'].split("/")
        print(projeto[4])
        PrUs = ProjetoUsuario()
        PrUs.usuario = Usuario.objects.get(pk=usuario[4])
        PrUs.projeto = Projeto.objects.get(pk=projeto[4])
        PrUs.save()
        bundle.obj = PrUs
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized('Não permitido.')


#            """ RESOURCE TAREFA """

class TarefaResource(ModelResource):
    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get','post', 'delete','put']
        aways_return_data = True
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        print(authentication)
        filtering = {
            "descricao": ('exact', 'startswith',)
        }

    def obj_create(self, bundle, **kwargs):
        nome = bundle.data['nome']
        usuario = bundle.data['usuario'].split("/")
        projeto = bundle.data['projeto'].split("/")
        TarefaProjeto = Tarefa.objects.filter(nome = nome, projeto = projeto[4])

        solicitante = bundle.request.user
        users = User.objects.get(pk = usuario[4])
        print(solicitante==users)

        if (TarefaProjeto.__len__() == 0):
            tarefa = Tarefa()
            tarefa.nome = bundle.data['nome']
            tarefa.projeto = Projeto.objects.get(pk=projeto[4])
            tarefa.usuario = User.objects.get(pk=usuario[4])
            tarefa.save()
            bundle.obj = tarefa
            return bundle
        else:
            raise Unauthorized('Já existe Tarefa cadastrada neste projeto.')

    def obj_delete(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk=kwargs['pk'])
        donoTarefa = User.objects.get(username=tarefa.usuario)
        solicitante = bundle.request.user
        if not(donoTarefa.pk == solicitante.pk):
            raise Unauthorized('Tarefa registrada por outro usuario.')
        else:
            tarefa.delete()
            bundle.obj = tarefa

    def obj_update(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk=kwargs['pk'])
        donoTarefa = User.objects.get(username=tarefa.usuario)
        solicitante = bundle.request.user
        if(donoTarefa.pk == solicitante.pk):
            nome = bundle.data['nome']
            usuario = bundle.data['usuario'].split("/")
            projeto = bundle.data['projeto'].split("/")
            TarefaProjeto = Tarefa.objects.filter(nome = nome, projeto = projeto[4])
            if(TarefaProjeto.__len__() == 0):
                tarefa.nome = bundle.data['nome']
                tarefa.usuario = User.objects.get(pk = usuario[4])
                tarefa.projeto = Projeto.objects.get(pk = projeto[4])
                tarefa.save()
                bundle.obj = tarefa
            else:
                raise Unauthorized('Tarefa já cadastrada neste projeto.')
        else:
            raise Unauthorized('Tarefa registrada por outro usuario.')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized('Não permitido.')
