from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from account.models import AccountType
from .models import Indexer, ProductInvestment, Investment
from .forms import InvestmentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.dateparse import parse_date


class ProductListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        products = ProductInvestment.objects.all()
        indexers = Indexer.objects.all()

        indexer = request.GET.get("indexer")
        if indexer:
            products = products.filter(indexer=indexer)

        minimum_value = request.GET.get("minimum_value")
        if minimum_value:
            products = products.filter(minimum_value__gte=float(minimum_value))

        final_date = request.GET.get("validate")
        if final_date:
            products = products.filter(final_date__lte=parse_date(final_date))

        is_premium = request.GET.get("is_premium")
        if is_premium:
            products = products.filter(is_premium=(is_premium == "True"))

        context = {
            "products": products,
            "indexers": indexers,
        }
        return render(request, "product_list.html", context)


class ProductDetailView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        context = {
            "product": product,
        }
        return render(request, "product_detail.html", context)


class InvestmentCreateView(LoginRequiredMixin, View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        form = InvestmentForm()
        context = {
            "form": form,
            "product": product,
        }
        return render(request, "investment_form.html", context)

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(ProductInvestment, id=product_id)
        form = InvestmentForm(request.POST)
        context = {
            "form": form,
            "product": product,
        }

        if product.is_premium and request.user.type not in [
            AccountType.ADMIN.value,
            AccountType.PREMIUM.value,
        ]:
            messages.error(
                request,
                "Você precisa ser um usuário\
                      premium para investir em produtos premium.",
            )
            return render(request, "investment_form.html", context)

        if not form.is_valid():
            messages.error(
                request, "Dados inválidos. Por favor, verifique o formulário."
            )
            return render(request, "investment_form.html", context)

        applied_value = form.cleaned_data.get("applied_value")
        account = request.user

        if applied_value < product.minimum_value:
            messages.error(
                request,
                """O valor de aplicação não pode ser
                menor que o valor mínimo do produto.""",
            )
            return render(request, "investment_form.html", context)

        if applied_value > account.balance:
            messages.error(
                request, "Saldo insuficiente para realizar este investimento."
            )
            return render(request, "investment_form.html", context)

        Investment.objects.create(
            account=account,
            product=product,
            applied_value=applied_value,
        )

        account.balance -= applied_value
        account.save()

        messages.success(request, "Investimento contratado com sucesso!")
        return redirect("my_investments")


class MyInvestmentsListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        investments = Investment.objects.filter(account=request.user)

        min_applied_value = request.GET.get("min_applied_value")
        min_income = request.GET.get("min_income")
        status = request.GET.get("status")
        initial_date = request.GET.get("initial_date")
        rescue_date = request.GET.get("rescue_date")

        if min_applied_value:
            investments = investments.filter(
                applied_value__gte=min_applied_value)
        if min_income:
            investments = investments.filter(
                accumulated_income__gte=min_income)
        if status:
            investments = investments.filter(status=status)
        if initial_date:
            investments = investments.filter(
                initial_date__gte=parse_date(initial_date)
                )
        if rescue_date:
            investments = investments.filter(
                rescue_date__lte=parse_date(rescue_date)
                )

        context = {
            "investments": investments,
        }
        return render(request, "my_investments.html", context)


class MyInvestmentsRescueView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        investment_id = kwargs.get("investment_id")
        investment = get_object_or_404(
            Investment, id=investment_id, account=request.user
        )

        try:
            total_amount = investment.rescue_investment()
            messages.success(
                request,
                f"""Investimento resgatado com sucesso! Total: {
                    total_amount:.2f}""",
            )
        except ValueError as e:
            print("Error")
            messages.error(request, str(e))

        return redirect("my_investments")
