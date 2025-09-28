"""Serviços relacionados ao Amazon SQS."""
import boto3
from botocore.exceptions import ClientError
from ..config import get_sqs_queue_url

def send_message_to_sqs(message: str) -> str:
    """Envia uma mensagem para a fila SQS.
    
    Args:
        message: Mensagem a ser enviada
        
    Returns:
        str: ID da mensagem enviada
        
    Raises:
        RuntimeError: Se houver erro ao enviar a mensagem
    """
    try:
        sqs = boto3.client('sqs', region_name='us-east-1')
        queue_url = get_sqs_queue_url()
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        
        return response['MessageId']
        
    except ClientError as e:
        raise RuntimeError(f"Erro ao enviar mensagem para SQS: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {e}")

def receive_and_delete_message_from_sqs() -> dict:
    """Recebe e deleta uma mensagem da fila SQS.
    
    Returns:
        dict: Dados da mensagem recebida ou None se não houver mensagens
        
    Raises:
        RuntimeError: Se houver erro ao receber/deletar a mensagem
    """
    try:
        sqs = boto3.client('sqs', region_name='us-east-1')
        queue_url = get_sqs_queue_url()
        
        # Receber mensagem da fila
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=1  # Short polling
        )
        
        messages = response.get('Messages', [])
        if not messages:
            return None
        
        message = messages[0]
        receipt_handle = message['ReceiptHandle']
        
        # Deletar mensagem da fila
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        
        return {
            'message_id': message['MessageId'],
            'body': message['Body'],
            'receipt_handle': receipt_handle
        }
        
    except ClientError as e:
        raise RuntimeError(f"Erro ao receber/deletar mensagem do SQS: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado: {e}")