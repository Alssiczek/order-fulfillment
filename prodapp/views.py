from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importowanie messages
from django.contrib.staticfiles import finders
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, FileResponse
from django.contrib.auth import views as auth_views
import io
from .forms import OrderForm, CustomAuthenticationForm  # Import OrderForm
from .models import Order, Part, Component, PartComponent
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image, Frame, PageTemplate


@login_required
def generate_pdf(request, part_no, serial_number):
    part = get_object_or_404(Part, part_no=part_no)
    part_components = PartComponent.objects.filter(part=part, part_serial_number=serial_number)

    # Użycie filter zamiast get
    order = Order.objects.filter(part_no=part_no, serial_number=serial_number).first()
    if not order:
        return HttpResponseNotFound("Order not found")

    # Tworzenie pliku PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Style
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(name='Custom', parent=styles['Normal'], alignment=1)  # Center alignment

    # Tworzenie nagłówka
    title = Paragraph(f"Podsumowanie komponentów dla partu: {part_no}", styles['Title'])
    subtitle = Paragraph(f"Numer seryjny partu: {serial_number}", styles['Heading2'])
    created_by = Paragraph(f"Stworzone przez: {order.created_by.username}", styles['Normal'])
    created_at = Paragraph(f"Data utworzenia: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])

    # Dodanie tytułu i nagłówka na środku
    elements.append(Spacer(1, 1.2 * inch))  # Dodanie odstępu między logo a tytułem
    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(subtitle)
    elements.append(Spacer(1, 12))
    elements.append(created_by)
    elements.append(created_at)
    elements.append(Spacer(1, 24))  # Dodanie odstępu przed tabelą

    # Tworzenie tabeli z komponentami
    data = [['Komponent', 'Numer seryjny']]
    for part_component in part_components:
        data.append([part_component.component.component_no, part_component.component_serial_number])

    table = Table(data, colWidths=[3 * inch, 3 * inch])  # Ustawienie szerokości kolumn

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Kolor tła nagłówka
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Kolor tekstu nagłówka
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Wyrównanie tekstu w komórkach
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Czcionka nagłówka
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Rozmiar czcionki nagłówka
        ('FONTSIZE', (0, 1), (-1, -1), 12),  # Rozmiar czcionki zawartości
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),  # Kolor tła zawartości
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Kolor siatki
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Dolne wypełnienie nagłówka
        ('TOPPADDING', (0, 0), (-1, 0), 12),  # Górne wypełnienie nagłówka
    ]))

    elements.append(table)

    # Funkcja layoutu dla dodania elementów na stronę
    def add_page_layout(canvas, doc):
        canvas.saveState()
        # Dodawanie logo na górze z lewej
        logo_path = finders.find('images/logo.png')  # Znajdź ścieżkę do logo
        if logo_path:
            canvas.drawImage(logo_path, inch, doc.pagesize[1] - 1.5 * inch, width=3 * inch, height=1 * inch, mask='auto')
        canvas.restoreState()

    # Dodanie layoutu do dokumentu
    doc.build(elements, onFirstPage=add_page_layout, onLaterPages=add_page_layout)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Podsumowanie_komponentow.pdf')
@login_required
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            part_no = form.cleaned_data['part_no']
            if not Part.objects.filter(part_no=part_no).exists():
                messages.error(request, 'Nie prawidłowy kod')
            else:
                order = form.save(commit=False)
                order.created_by = request.user  # Przypisz instancję użytkownika
                order.save()
                serial_number = form.cleaned_data['serial_number']
                return redirect('scan_components', part_no=part_no, serial_number=serial_number)
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


@login_required
def scan_components(request, part_no, serial_number):
    part = get_object_or_404(Part, part_no=part_no)
    components = part.components.all()

    component_counts = []
    all_scanned = True
    for component in components:
        scanned_count = PartComponent.objects.filter(part=part, part_serial_number=serial_number,
                                                     component=component).count()
        component_counts.append({
            'component': component,
            'scanned_count': scanned_count
        })
        if scanned_count != component.quantity:
            all_scanned = False

    if request.method == 'POST':
        component_no = request.POST.get('component_no').strip()
        component_serial_number = request.POST.get('component_serial_number').strip()

        try:
            component = Component.objects.get(part=part, component_no=component_no)
            PartComponent.objects.create(
                part=part,
                part_serial_number=serial_number,
                component=component,
                component_serial_number=component_serial_number
            )
            return redirect('scan_components', part_no=part_no, serial_number=serial_number)
        except Component.DoesNotExist:
            messages.error(request, 'Zły komponent!')

    return render(request, 'scan_components.html', {
        'part': part,
        'component_counts': component_counts,
        'serial_number': serial_number,
        'all_scanned': all_scanned
    })


@login_required
def remove_component(request, part_no, serial_number, component_id):
    part_component = get_object_or_404(PartComponent, id=component_id, part__part_no=part_no,
                                       part_serial_number=serial_number)
    part_component.delete()
    return redirect('scan_components', part_no=part_no, serial_number=serial_number)

@login_required
def complete_order(request, part_no, serial_number):
    # Logika do obsługi zakończenia zamówienia
    # Możesz dodać tutaj dodatkowe przetwarzanie, np. oznaczenie zamówienia jako zakończonego w bazie danych
    return redirect('add_order')




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Przekierowanie na stronę główną
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class LoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm