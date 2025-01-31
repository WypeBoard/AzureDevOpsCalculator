from typing import List, Optional
from pydantic import BaseModel


class Repository(BaseModel):
    id: str
    name: str
    url: str

class CreatedBy(BaseModel):
    id: str
    displayName: str
    uniqueName: str
    url: str
    imageUrl: str

class PullRequest(BaseModel):
    pullRequestId: int
    codeReviewId: int
    status: str
    createdBy: CreatedBy
    creationDate: str
    title: str
    description: Optional[str] = None
    sourceRefName: str
    targetRefName: str
    mergeStatus: Optional[str] = None
    repository: Repository
    url: str
    
    class Config:
        extra = 'ignore'


class Comment(BaseModel):
    id: int
    parentCommentId: Optional[int] = None
    commentType: str
    content: Optional[str] = None

    @property
    def is_reply(self) -> bool:
        return self.parentCommentId is not None
    
class Thread(BaseModel):
    id: int
    publishedDate: str
    lastUpdatedDate: str
    comments: List[Comment]
    
    class Config:
        extra = 'ignore'

    
class PullRequests(BaseModel):
    id: int
    base: PullRequest
    threads: List[Thread] = None
    
    def add_threads(self, threads: List[Thread]):
        self.threads.extend(threads)
