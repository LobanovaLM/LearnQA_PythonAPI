FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -s --alluredir=test_results/ /LearnQA_PythonAPI/test/