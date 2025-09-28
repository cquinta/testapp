"""Rotas de mensageria."""
from fastapi import APIRouter, HTTPException, status

from ..models import MessageRequest, MessageResponse, ReceiveMessageResponse
from ..services.sqs_service import send_message_to_sqs, receive_and_delete_message_from_sqs
from ..config import get_sqs_queue_url

router = APIRouter(tags=["Messaging"])

@router.post(
    "/sent-message",
    response_model=MessageResponse,
    summary="Enviar mensagem para SQS",
    description="Envia uma mensagem para a fila SQS configurada na variável de ambiente SQS_QUEUE_URL",
    response_description="Confirmação do envio da mensagem com ID gerado"
)
def sent_message(request: MessageRequest) -> MessageResponse:
    """Endpoint que envia uma mensagem para a fila SQS.
    
    Args:
        request: Dados da mensagem a ser enviada
        
    Returns:
        MessageResponse: Confirmação do envio com ID da mensagem
        
    Raises:
        HTTPException: 500 se houver erro ao enviar a mensagem
        HTTPException: 400 se a configuração SQS estiver inválida
    """
    try:
        queue_url = get_sqs_queue_url()
        message_id = send_message_to_sqs(request.message)
        
        return MessageResponse(
            status="success",
            message_id=message_id,
            queue_url=queue_url
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/receive-message",
    response_model=ReceiveMessageResponse,
    summary="Receber mensagem do SQS",
    description="Recebe e deleta uma mensagem da fila SQS configurada na variável de ambiente SQS_QUEUE_URL",
    response_description="Mensagem recebida da fila ou indicação de fila vazia"
)
def receive_message() -> ReceiveMessageResponse:
    """Endpoint que recebe e deleta uma mensagem da fila SQS.
    
    Returns:
        ReceiveMessageResponse: Mensagem recebida ou indicação de fila vazia
        
    Raises:
        HTTPException: 500 se houver erro ao receber a mensagem
        HTTPException: 400 se a configuração SQS estiver inválida
    """
    try:
        queue_url = get_sqs_queue_url()
        message_data = receive_and_delete_message_from_sqs()
        
        if message_data is None:
            return ReceiveMessageResponse(
                status="empty",
                queue_url=queue_url,
                message="Nenhuma mensagem disponível na fila"
            )
        
        return ReceiveMessageResponse(
            status="success",
            message_id=message_data['message_id'],
            body=message_data['body'],
            queue_url=queue_url,
            message="Mensagem recebida e removida da fila com sucesso"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )