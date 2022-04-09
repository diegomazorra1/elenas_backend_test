import factory
from tasks.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: "title_{}".format(n))
    description = "Description"

    class Meta:
        model = Task
