from pydantic import BaseModel, Field

class AddAnswer(BaseModel):
    question_id: int = Field(..., alias='question_id')
    content: str = Field(..., alias='content')

class AddQuestion(BaseModel):
    title: str = Field(..., alias = 'title')
    content: str = Field(..., alias = 'content')

class DeleteQuestion(BaseModel):
    question_id: int = Field(..., alias='question_id')

class DeleteAnswer(BaseModel):
    answer_id: int = Field(..., alias='answer_id')