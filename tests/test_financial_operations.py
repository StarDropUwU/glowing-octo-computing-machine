import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from src.services.services import financialService
from src.models import  FinancialOperation
from src.app import app

class TestGetOperations(unittest.TestCase):
    
    @patch('src.services.services.session')
    def test_get_operations(self, mock_session):

        mock_operation = MagicMock(spec=FinancialOperation)
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        
        mock_operations = [mock_operation]

        mock_session.scalars.return_value = mock_operations
        
        data = {
            "tipo_operacao": "tipo_test",
            "valor": 100.0,
            "descricao": "test",
            "data": "2024-01-01"
        }

        with app.app_context():
            response, status_code = financialService.get_operations(page=1, per_page=10, data=data)
            
            mock_session.scalars.assert_called_once()
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, [mock_operation.create_exportable()])

class TestCreateOperation(unittest.TestCase):
    
    @patch('src.services.services.session')
    @patch('src.services.services.validate_operation_data')
    @patch('src.services.services.FinancialOperation')
    @patch('src.services.services.TransactionHistory')
    def test_create_operation_success(self, mock_transaction_history, mock_financial_operation, mock_validate_operation_data, mock_session):
        mock_validate_operation_data.return_value = True
        
        mock_operation = MagicMock()
        mock_operation.id = 1
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        mock_financial_operation.return_value = mock_operation
        
        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history
        
        data = {
            "tipo_operacao": "tipo_test",
            "valor": 100.0,
            "descricao": "test description",
            "data": "2024-01-01"
        }
        with app.app_context():

            response, status_code = financialService.create_operation(data)
            
            mock_validate_operation_data.assert_called_once_with(data)
            mock_financial_operation.assert_called_once_with(**data)
            mock_session.add.assert_any_call(mock_operation)
            mock_session.commit.assert_any_call()
            mock_transaction_history.assert_called_once()
            self.assertEqual(mock_history.operation_id, 1)
            self.assertEqual(mock_history.mudancas, "Criado")
            mock_session.add.assert_any_call(mock_history)
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, mock_operation.create_exportable())

    def test_create_operation_invalid_data(self):
        with patch('src.services.services.validate_operation_data') as mock_validate:
            mock_validate.return_value = False
            
            with app.app_context():
                response, status_code = financialService.create_operation({})
                mock_validate.assert_called_once()
                self.assertEqual(status_code, 400)
                self.assertEqual(response.json, {"error": "Invalid data"})


class TestGetSingularOperation(unittest.TestCase):

    @patch('src.services.services.session')
    def test_get_singular_operation_found(self, mock_session):
        mock_operation = MagicMock(spec=FinancialOperation)
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        
        mock_session.scalars.return_value.one_or_none.return_value = mock_operation

        with app.app_context():
        
            response, status_code = financialService.get_singular_operation(1)

            mock_session.scalars.assert_called_once()  
            mock_session.scalars.return_value.one_or_none.assert_called_once() 

            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, mock_operation.create_exportable())
    
    @patch('src.services.services.session')  
    def test_get_singular_operation_not_found(self, mock_session):
        mock_session.scalars.return_value.one_or_none.return_value = None
        
        with app.app_context():
            response, status_code = financialService.get_singular_operation(999)
            mock_session.scalars.assert_called_once()  
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Nenhuma operacao encontrada"})


class TestUpdateOperation(unittest.TestCase):
    
    @patch('src.services.services.session') 
    @patch('src.services.services.validate_operation_data')
    @patch('src.services.services.TransactionHistory')
    def test_update_operation_success(self, mock_transaction_history, mock_validate_operation_data, mock_session):
        mock_validate_operation_data.return_value = True

        mock_operation = MagicMock()
        mock_operation.id = 1
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }

        mock_session.scalars.return_value.one_or_none.return_value = mock_operation

        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history
        
        data = {
            "tipo_operacao": "tipo_updated",
            "valor": 200.0,
            "descricao": "updated description",
            "data": "2024-01-02"
        }

        with app.app_context():

            response, status_code = financialService.update_operation(1, data)
            
            mock_validate_operation_data.assert_called_once_with(data)
            mock_session.scalars.assert_called_once()
            mock_session.scalars.return_value.one_or_none.assert_called_once() 
          
            self.assertEqual(mock_operation.tipo_operacao, data["tipo_operacao"])
            self.assertEqual(mock_operation.valor, data["valor"])
            self.assertEqual(mock_operation.descricao, data["descricao"])
            
            self.assertEqual(mock_session.commit.call_count, 2)
            
            mock_transaction_history.assert_called_once()
            self.assertEqual(mock_history.operation_id, 1)
            self.assertEqual(mock_history.mudancas, "Alterado")
            mock_session.add.assert_any_call(mock_history)
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, mock_operation.create_exportable())

    @patch('src.services.services.session') 
    @patch('src.services.services.validate_operation_data')
    def test_update_operation_invalid_data(self, mock_validate, mock_session):

        mock_validate.return_value = False
        
        with app.app_context():

            
            response, status_code = financialService.update_operation(1, {})
            
            
            mock_validate.assert_called_once_with({})
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json, {"error": "Invalid data"})
            
            
            mock_session.scalars.assert_not_called()
            mock_session.commit.assert_not_called()

    @patch('src.services.services.session')
    @patch('src.services.services.validate_operation_data')
    def test_update_operation_not_found(self, mock_validate, mock_session):
        mock_validate.return_value = True
        
        mock_session.scalars.return_value.one_or_none.return_value = None
        
        with app.app_context():

            response, status_code = financialService.update_operation(999, {"tipo_operacao": "test"})
          
            mock_validate.assert_called_once_with({"tipo_operacao": "test"})
            mock_session.scalars.assert_called_once()
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Nenhuma operacao encontrada"})
            
            mock_session.commit.assert_not_called()
            mock_session.add.assert_not_called()


class TestDeleteOperation(unittest.TestCase):
    
    @patch('src.services.services.session')
    @patch('src.services.services.TransactionHistory') 
    def test_delete_operation_success(self, mock_transaction_history, mock_session):
        mock_operation = MagicMock()
        mock_operation.id = 1
        
        mock_session.scalars.return_value.one_or_none.return_value = mock_operation
        
        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history

        with app.app_context():
        
            response, status_code = financialService.delete_operation(1)
            
            mock_session.scalars.assert_called_once() 
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            mock_session.delete.assert_called_once_with(mock_operation)
            self.assertEqual(mock_session.commit.call_count, 2) 
            
            mock_transaction_history.assert_called_once()
            self.assertEqual(mock_history.operation_id, 1)
            self.assertEqual(mock_history.mudancas, "Deletado")
            mock_session.add.assert_any_call(mock_history)
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, {"success": 'Operação de id 1 deletada com sucesso'})

    @patch('src.services.services.session')
    @patch('src.services.services.TransactionHistory')
    def test_delete_operation_not_found(self, mock_transaction_history, mock_session):
        mock_session.scalars.return_value.one_or_none.return_value = None

        with app.app_context():
            response, status_code = financialService.delete_operation(999)
    
            mock_session.scalars.assert_called_once()
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Operação não encontrada"})
            
            mock_session.delete.assert_not_called()
            mock_session.commit.assert_not_called()
            mock_session.add.assert_not_called()


class TestCreateBulkOperation(unittest.TestCase):
    
    @patch('src.services.services.session')
    @patch('src.services.services.validate_operation_data') 
    def test_create_bulk_operation_no_data(self, mock_validate, mock_session):
        
        data = []

        with app.app_context():
            response, status_code = financialService.create_bulk_operation(data)
            
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json, {"error": "Invalid data: no items in List"})
            
            mock_session.add_all.assert_not_called()
            mock_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()