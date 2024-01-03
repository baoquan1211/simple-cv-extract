from typing import Any
from django.shortcuts import render
from rest_framework import viewsets, status, response
import io
from django.http import FileResponse
from pdfminer.high_level import extract_text
from services.cv_extraction_service import CvExtractionService
from exceptions.exceptions import ServiceException
import threading

# Create your views here.


class CvExtractorView(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.cv_extraction_service = CvExtractionService(
            "https://aiservice.fujinet.net/api/v2/nlp/cv-extraction"
        )

    def _request(self, content: str, result: list):
        try:
            res = self.cv_extraction_service.request(content)
            print(res)
            result.append(res)
        except ServiceException as ex:
            return response.Response(
                data={"error": ex.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        data = request.FILES
        byte_file = io.BytesIO(data["file"].read())
        text = extract_text(pdf_file=byte_file)
        texts = text.split("\n\n")
        texts = map(lambda s: s.strip(), texts)
        text_list = []
        for text in texts:
            if text != "":
                text_list.append(text)

        text_list_for_request = []
        i = 0
        text_list_for_request.append("")
        for text in text_list:
            if len(text_list_for_request[i]) + len(text) < 500:
                tmp = text_list_for_request[i] + " " + text
                text_list_for_request[i] = tmp.strip()
            else:
                i = i + 1
                text_list_for_request.append(text)
        result = []
        # list_thread = []
        # for text in text_list_for_request:
        #     thread = threading.Thread(target=self._request, args=(text, result))
        #     list_thread.append(thread)

        # for thread in list_thread:
        #     thread.start()
        # for thread in list_thread:
        #     thread.join()

        data_response = {"name": "", "programming_languages": set(), "framework": set()}
        for text in text_list_for_request:
            try:
                res = self.cv_extraction_service.request(text)
                for item in res:
                    if item["label"] == "NAME":
                        data_response["name"] = text[int(item["start"]) : item["end"]]
                    elif item["label"] == "PLANG":
                        data_response["programming_languages"].add(
                            text[int(item["start"]) : item["end"]]
                        )
                    elif item["label"] == "FRAMEWORK":
                        data_response["framework"].add(
                            text[int(item["start"]) : item["end"]]
                        )
            except ServiceException as ex:
                return response.Response(
                    data={"error": ex.message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return response.Response(data_response, status=status.HTTP_200_OK)
