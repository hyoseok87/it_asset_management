# views.py
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Asset, AssetHistory
from .forms import AssetForm, UserRegisterForm
import csv
from django.http import HttpResponse
import io

from django.http import JsonResponse

@login_required
def asset_list(request):
    query = request.GET.get('q')
    asset_type = request.GET.get('asset_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    active_tab = request.GET.get('active_tab', 'Verwaltung')

    filters = Q()
    if query:
        filters &= Q(name__icontains=query)
    if asset_type:
        filters &= Q(asset_type__iexact=asset_type)
    if start_date:
        filters &= Q(purchase_date__gte=start_date)
    if end_date:
        filters &= Q(purchase_date__lte=end_date)

    filtered_assets = Asset.objects.filter(filters) if (query or asset_type or start_date or end_date) else None
    all_assets = Asset.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        asset_data = [{'name': asset.name, 'asset_type': asset.get_asset_type_display(), 'purchase_date': asset.purchase_date} for asset in (filtered_assets or [])]
        return JsonResponse({'assets': asset_data})

    return render(request, 'asset_management/asset_list.html',
                  {'filtered_assets': filtered_assets, 'all_assets': all_assets, 'query': query, 'asset_type': asset_type,
                   'start_date': start_date, 'end_date': end_date, 'active_tab': active_tab})



@login_required
def export_assets_csv(request):
    assets = Asset.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Asset Type', 'Location', 'Purchase Date', 'Price'])
    for asset in assets:
        writer.writerow([asset.name, asset.get_asset_type_display(), asset.location, asset.purchase_date, asset.price])

    return response



@login_required
def import_assets_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'asset_management/asset_list.html', {'error': 'File is not CSV type'})

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)  # Skip header row
        for column in csv.reader(io_string, delimiter=',', quotechar='"'):
            try:
                _, created = Asset.objects.update_or_create(
                    name=column[0],
                    asset_type=column[1],
                    location=column[2],
                    purchase_date=column[3],
                    defaults={'price': column[4]}
                )
            except Exception as e:
                return render(request, 'asset_management/asset_list.html', {'error': f'Error on row: {column}, Error: {str(e)}'})
        return redirect('asset_list')
    return render(request, 'asset_management/asset_list.html')





@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    history = AssetHistory.objects.filter(asset=asset).order_by('-change_date')
    return render(request, 'asset_management/asset_detail.html', {'asset': asset, 'history': history})


@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'asset_management/asset_form.html', {'form': form})


@login_required
def asset_edit(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'asset_management/asset_form.html', {'form': form})


@login_required
def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'asset_management/asset_confirm_delete.html', {'asset': asset})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('asset_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})