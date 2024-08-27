import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from src.services.services import financialService
from src.models import  FinancialOperation
from flask import jsonify
from src.app import app  # Import your Flask app creation function

class TestGetOperations(unittest.TestCase):
    
    @patch('src.services.services.session')  # Mock the session
    def test_get_operations(self, mock_session):
        # Create the Flask app instance

        # Set up mock data and behavior
        mock_operation = MagicMock(spec=FinancialOperation)
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        
        mock_operations = [mock_operation]
        
        # Mock the query chain
        mock_session.scalars.return_value = mock_operations
        
        # Define input data
        data = {
            "tipo_operacao": "tipo_test",
            "valor": 100.0,
            "descricao": "test",
            "data": "2024-01-01"
        }

        # Use the application context
        with app.app_context():
            # Call the function
            response, status_code = financialService.get_operations(page=1, per_page=10, data=data)
            
            # Assertions
            mock_session.scalars.assert_called_once()  # Ensure scalars() was called
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, [mock_operation.create_exportable()])

class TestCreateOperation(unittest.TestCase):
    
    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.validate_operation_data')  # Mock the validation function
    @patch('src.services.services.FinancialOperation')  # Mock the FinancialOperation model
    @patch('src.services.services.TransactionHistory')  # Mock the TransactionHistory model
    def test_create_operation_success(self, mock_transaction_history, mock_financial_operation, mock_validate_operation_data, mock_session):
        # Mock the validate_operation_data to return True
        mock_validate_operation_data.return_value = True
        
        # Mock the FinancialOperation instance
        mock_operation = MagicMock()
        mock_operation.id = 1
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        mock_financial_operation.return_value = mock_operation
        
        # Mock the TransactionHistory instance
        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history
        
        # Define input data
        data = {
            "tipo_operacao": "tipo_test",
            "valor": 100.0,
            "descricao": "test description",
            "data": "2024-01-01"
        }
        with app.app_context():

        # Call the function
            response, status_code = financialService.create_operation(data)
            
            # Assertions
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
        # Similar to the previous test, but mock `validate_operation_data` to return False
        with patch('src.services.services.validate_operation_data') as mock_validate:
            mock_validate.return_value = False
            
            with app.app_context():
            # Call the function
                response, status_code = financialService.create_operation({})
                
                # Assertions
                mock_validate.assert_called_once()
                self.assertEqual(status_code, 400)
                self.assertEqual(response.json, {"error": "Invalid data"})


class TestGetSingularOperation(unittest.TestCase):

    @patch('src.services.services.session')  # Mock the session
    def test_get_singular_operation_found(self, mock_session):
        # Mock the FinancialOperation instance
        mock_operation = MagicMock(spec=FinancialOperation)
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        
        # Mock the query chain to return the mock_operation
        mock_session.scalars.return_value.one_or_none.return_value = mock_operation

        with app.app_context():
        
            # Call the function with a valid ID
            response, status_code = financialService.get_singular_operation(1)

            # Assertions
            mock_session.scalars.assert_called_once()  # Ensure scalars() was called
            mock_session.scalars.return_value.one_or_none.assert_called_once()  # Ensure one_or_none() was called

            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, mock_operation.create_exportable())
    
    @patch('src.services.services.session')  # Mock the session
    def test_get_singular_operation_not_found(self, mock_session):
        # Mock the query chain to return None
        mock_session.scalars.return_value.one_or_none.return_value = None
        
        with app.app_context():

            # Call the function with an ID that doesn't exist
            response, status_code = financialService.get_singular_operation(999)
            
            # Assertions
            mock_session.scalars.assert_called_once()  # Ensure scalars() was called
            mock_session.scalars.return_value.one_or_none.assert_called_once()  # Ensure one_or_none() was called
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Nenhuma operacao encontrada"})


class TestUpdateOperation(unittest.TestCase):
    
    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.validate_operation_data')  # Mock the validation function
    @patch('src.services.services.TransactionHistory')  # Mock the TransactionHistory model
    def test_update_operation_success(self, mock_transaction_history, mock_validate_operation_data, mock_session):
        # Mock the validate_operation_data to return True
        mock_validate_operation_data.return_value = True
        
        # Mock the FinancialOperation instance
        mock_operation = MagicMock()
        mock_operation.id = 1
        mock_operation.create_exportable.return_value = {
            'tipo_operacao': 'tipo_test',
            'valor': 100.0,
            'descricao': 'test description',
            'data': '2024-01-01'
        }
        
        # Mock the query chain to return the mock_operation
        mock_session.scalars.return_value.one_or_none.return_value = mock_operation
        
        # Mock the TransactionHistory instance
        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history
        
        # Define input data
        data = {
            "tipo_operacao": "tipo_updated",
            "valor": 200.0,
            "descricao": "updated description",
            "data": "2024-01-02"
        }

        with app.app_context():

            # Call the function
            response, status_code = financialService.update_operation(1, data)
            
            # Assertions
            mock_validate_operation_data.assert_called_once_with(data)
            mock_session.scalars.assert_called_once()  # Ensure scalars() was called
            mock_session.scalars.return_value.one_or_none.assert_called_once()  # Ensure one_or_none() was called
            
            # Verify updates
            self.assertEqual(mock_operation.tipo_operacao, data["tipo_operacao"])
            self.assertEqual(mock_operation.valor, data["valor"])
            self.assertEqual(mock_operation.descricao, data["descricao"])
            
            # Ensure session.commit() was called twice
            self.assertEqual(mock_session.commit.call_count, 2)
            
            mock_transaction_history.assert_called_once()
            self.assertEqual(mock_history.operation_id, 1)
            self.assertEqual(mock_history.mudancas, "Alterado")
            mock_session.add.assert_any_call(mock_history)
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, mock_operation.create_exportable())

    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.validate_operation_data')  # Mock the validation function
    def test_update_operation_invalid_data(self, mock_validate, mock_session):
        # Mock the validate_operation_data to return False
        mock_validate.return_value = False
        
        with app.app_context():

            # Call the function with invalid data
            response, status_code = financialService.update_operation(1, {})
            
            # Assertions
            mock_validate.assert_called_once_with({})
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json, {"error": "Invalid data"})
            
            # Ensure no database operations were performed
            mock_session.scalars.assert_not_called()
            mock_session.commit.assert_not_called()

    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.validate_operation_data')  # Mock the validation function
    def test_update_operation_not_found(self, mock_validate, mock_session):
        # Mock the validate_operation_data to return True
        mock_validate.return_value = True
        
        # Mock the query chain to return None
        mock_session.scalars.return_value.one_or_none.return_value = None
        
        with app.app_context():

            # Call the function with a non-existent ID
            response, status_code = financialService.update_operation(999, {"tipo_operacao": "test"})
            
            # Assertions
            mock_validate.assert_called_once_with({"tipo_operacao": "test"})
            mock_session.scalars.assert_called_once()
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Nenhuma operacao encontrada"})
            
            # Ensure no commit or history addition was performed
            mock_session.commit.assert_not_called()
            mock_session.add.assert_not_called()


class TestDeleteOperation(unittest.TestCase):
    
    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.TransactionHistory')  # Mock the TransactionHistory model
    def test_delete_operation_success(self, mock_transaction_history, mock_session):
        # Mock the FinancialOperation instance
        mock_operation = MagicMock()
        mock_operation.id = 1
        
        # Mock the query chain to return the mock_operation
        mock_session.scalars.return_value.one_or_none.return_value = mock_operation
        
        # Mock the TransactionHistory instance
        mock_history = MagicMock()
        mock_transaction_history.return_value = mock_history

        with app.app_context():
        
            # Call the function
            response, status_code = financialService.delete_operation(1)
            
            # Assertions
            mock_session.scalars.assert_called_once()  # Ensure scalars() was called
            mock_session.scalars.return_value.one_or_none.assert_called_once()  # Ensure one_or_none() was called
            
            # Verify delete and add operations
            mock_session.delete.assert_called_once_with(mock_operation)
            self.assertEqual(mock_session.commit.call_count, 2)  # Ensure commit was called twice
            
            mock_transaction_history.assert_called_once()
            self.assertEqual(mock_history.operation_id, 1)
            self.assertEqual(mock_history.mudancas, "Deletado")
            mock_session.add.assert_any_call(mock_history)
            
            self.assertEqual(status_code, 200)
            self.assertEqual(response.json, {"success": 'Operação de id 1 deletada com sucesso'})

    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.TransactionHistory')  # Mock the TransactionHistory model
    def test_delete_operation_not_found(self, mock_transaction_history, mock_session):
        # Mock the query chain to return None
        mock_session.scalars.return_value.one_or_none.return_value = None

        with app.app_context():
        
            # Call the function with a non-existent ID
            response, status_code = financialService.delete_operation(999)
            
            # Assertions
            mock_session.scalars.assert_called_once()
            mock_session.scalars.return_value.one_or_none.assert_called_once()
            
            self.assertEqual(status_code, 404)
            self.assertEqual(response.json, {"error": "Operação não encontrada"})
            
            # Ensure no delete or history addition was performed
            mock_session.delete.assert_not_called()
            mock_session.commit.assert_not_called()
            mock_session.add.assert_not_called()


class TestCreateBulkOperation(unittest.TestCase):
    
    @patch('src.services.services.session')  # Mock the session
    @patch('src.services.services.validate_operation_data')  # Mock the validation function
    def test_create_bulk_operation_no_data(self, mock_validate, mock_session):
        # Define empty data
        data = []

        with app.app_context():
        
            # Call the function with empty data
            response, status_code = financialService.create_bulk_operation(data)
            
            # Assertions
            self.assertEqual(status_code, 400)
            self.assertEqual(response.json, {"error": "Invalid data: no items in List"})
            
            # Ensure no add_all or commit was performed
            mock_session.add_all.assert_not_called()
            mock_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()