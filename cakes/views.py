import xlwt

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView

from cakes.helpers import fetch_all_cakes
from cakes.models import Cake, Category


class CakeView(View):

    def get(self, request, *args, **kwargs):
        cakes = Cake.objects.all()
        categories = Category.objects.all()

        category_id = request.GET.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            cakes = category.cakes.all()
        return render(request, 'home.html', {'cakes': cakes, 'categories': categories})


class FetchCakes(View):

    def get(self, request, *args, **kwargs):
        fetch_all_cakes()
        return redirect(reverse('home'))


class ExportCakes(View):

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('format')
        if export_format == 'json':
            categories = Category.objects.all()
            for category in categories:
        elif export_format == 'excel':
            categories = Category.objects.all()
            workbook = xlwt.Workbook()
            for category in categories:
                worksheet = workbook.add_sheet(category.name)
                worksheet.write(0, 0, '#')
                worksheet.write(0, 1, 'Title')
                worksheet.write(0, 2, 'Image')
                cakes = category.cakes.all()
                for row, cake in enumerate(cakes, start=1):
                    worksheet.write(row, 0, row)
                    worksheet.write(row, 1, cake.title)
                    worksheet.write(row, 2, cake.image.url)
                    worksheet.write(row, 3, cake.price)
            filename = 'cakes.xls'
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=' + filename
            workbook.save(response)
            return response
        else:
            return HttpResponse('Invalid format', status=400)