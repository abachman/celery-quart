# notes on a generative AI chat streaming response protocol

should have:

All responses, error or success, should consistent response headers:

```
Content-Type: application/json-lines
Trransfer-Encoding: chunked
```

The goal of a successful response is to communicate the state of the system to the client in as close to real time as possible.

Each chunk or line or JSON object of the response should be useful for composing a whole response state within the client.

The most significant concern of any streaming chat-like generative AI system is the text of the model's response, often referred to with the label `content`.

Different kinds kinds of responses may add their own metadata so a response should also indicate what kind of response it is. We can refer to the "metadata of the response" as the `context` of the response. Similar to the text `content`, `context` can grow during a response stream.

RAG search, for example, is going to produce a context which includes chunks of documents that will be used within the prompt that was actually sent to the large language mod.

## Microsoft Azure Guidance

source: https://github.com/Azure-Samples/ai-chat-protocol?tab=readme-ov-file#streaming-response

> Here's an example of the first three JSON objects in a streaming response:

```json
{
    "delta": {
        "role": "assistant"
    },
    "context": {
        "data_points": {
            "text": [
                "Benefit_Options.pdf#page=3:  The plans also cover preventive care services such as mammograms, colonoscopies, and  other cancer screenings...(truncated)",
                "Benefit_Options.pdf#page=3:   Both plans offer coverage for medical services. Northwind Health Plus offers coverage for hospital stays,  doctor visits,...(truncated)",
                "Benefit_Options.pdf#page=3:  With Northwind Health Plus, you can choose  from a variety of in -network providers, including primary care physicians,...(truncated)"
            ]
        },
        "thoughts": [
            {
                "title": "Original user query",
                "description": "What is included in my Northwind Health Plus plan that is not in standard?",
                "props": null
            },
            {
                "title": "Generated search query",
                "description": "Northwind Health Plus plan standard",
                "props": {
                    "use_semantic_captions": false,
                    "has_vector": false
                }
            },
            {
                "title": "Results",
                "description": [
                    {
                        "id": "file-Benefit_Options_pdf-42656E656669745F4F7074696F6E732E706466-page-2",
                        "content": " The plans also cover preventive care services such as mammograms, colonoscopies, and \nother cancer screenings...(truncated)",
                        "embedding": null,
                        "imageEmbedding": null,
                        "category": null,
                        "sourcepage": "Benefit_Options.pdf#page=3",
                        "sourcefile": "Benefit_Options.pdf",
                        "oids": [],
                        "groups": [],
                        "captions": []
                    },
                    {
                        "id": "file-Benefit_Options_pdf-42656E656669745F4F7074696F6E732E706466-page-3",
                        "content": " \nBoth plans offer coverage for medical services. Northwind Health Plus offers coverage for hospital stays, \ndoctor visits,...(truncated)",
                        "embedding": null,
                        "imageEmbedding": null,
                        "category": null,
                        "sourcepage": "Benefit_Options.pdf#page=3",
                        "sourcefile": "Benefit_Options.pdf",
                        "oids": [],
                        "groups": [],
                        "captions": []
                    },
                    {
                        "id": "file-Benefit_Options_pdf-42656E656669745F4F7074696F6E732E706466-page-1",
                        "content": " With Northwind Health Plus, you can choose \nfrom a variety of in -network providers, including primary care physicians,...(truncated)",
                        "embedding": null,
                        "imageEmbedding": null,
                        "category": null,
                        "sourcepage": "Benefit_Options.pdf#page=3",
                        "sourcefile": "Benefit_Options.pdf",
                        "oids": [],
                        "groups": [],
                        "captions": []
                    }
                ],
                "props": null
            },
            {
                "title": "Prompt",
                "description": [
                    "{'role': 'system', 'content': \"Assistant helps the company employees with their healthcare plan questions, and questions about the employee handbook. Be brief in your answers.\\n        Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.\\n        For tabular information return it as an html table. Do not return markdown format. If the question is not in English, answer in the language used in the question.\\n        Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, for example [info1.txt]. Don't combine sources, list each source separately, for example [info1.txt][info2.pdf].\\n        \\n        \\n        \"}",
                    "{'role': 'user', 'content': 'What is included in my Northwind Health Plus plan that is not in standard?'}",
                    "{'role': 'assistant', 'content': 'There is no specific information provided about what is included in the Northwind Health Plus plan that is not in the standard plan. It is recommended to read the plan details carefully and ask questions to understand the specific benefits of the Northwind Health Plus plan [Northwind_Standard_Benefits_Details.pdf#page=91].'}",
                    "{'role': 'user', 'content': \"What is included in my Northwind Health Plus plan that is not in standard?\\n\\nSources:\\nBenefit_Options.pdf#page=3:  The plans also cover preventive care services such as mammograms, colonoscopies, and  other cancer screenings...(truncated)\\nBenefit_Options.pdf#page=3:   Both plans offer coverage for medical services. Northwind Health Plus offers coverage for hospital stays,  doctor visits,...(truncated)\\nBenefit_Options.pdf#page=3:  With Northwind Health Plus, you can choose  from a variety of in -network providers, including primary care physicians,...(truncated)\"}"
                ],
                "props": null
            }
        ]
    },
    "session_state": null,
}
{
    "delta": {
        "content": null,
        "function_call": null,
        "role": "assistant",
        "tool_calls": null
    }
}
{
    "delta": {
        "content": "The",
        "function_call": null,
        "role": null,
        "tool_calls": null
    }
}
```
