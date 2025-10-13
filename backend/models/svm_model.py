"""
SVM Classifier for Sketch Matching
"""
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging
import os

logger = logging.getLogger(__name__)

class SVMSketchMatcher:
    """
    SVM-based sketch matching system
    Matches sketches to criminal records using feature vectors
    """
    
    def __init__(self, kernel='rbf', C=1.0, gamma='scale'):
        """
        Initialize SVM classifier
        
        Args:
            kernel: Kernel type ('linear', 'rbf', 'poly')
            C: Regularization parameter
            gamma: Kernel coefficient
        """
        self.classifier = svm.SVC(
            kernel=kernel,
            C=C,
            gamma=gamma,
            probability=True,  # Enable probability estimates
            class_weight='balanced'
        )
        
        self.scaler = StandardScaler()
        self.is_trained = False
        
        logger.info(f"SVM Matcher initialized with kernel={kernel}, C={C}, gamma={gamma}")
    
    def train(self, X_train, y_train, validation_split=0.2):
        """
        Train the SVM classifier
        
        Args:
            X_train: Training features (N x feature_dim)
            y_train: Training labels (N,)
            validation_split: Validation set size
        
        Returns:
            Training metrics
        """
        try:
            logger.info(f"Training SVM with {len(X_train)} samples...")
            
            # Split data
            X_train_split, X_val, y_train_split, y_val = train_test_split(
                X_train, y_train, test_size=validation_split, random_state=42, stratify=y_train
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train_split)
            X_val_scaled = self.scaler.transform(X_val)
            
            # Train classifier
            self.classifier.fit(X_train_scaled, y_train_split)
            
            # Validate
            train_pred = self.classifier.predict(X_train_scaled)
            val_pred = self.classifier.predict(X_val_scaled)
            
            train_acc = accuracy_score(y_train_split, train_pred)
            val_acc = accuracy_score(y_val, val_pred)
            
            self.is_trained = True
            
            logger.info(f"Training complete - Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")
            
            return {
                'train_accuracy': train_acc,
                'val_accuracy': val_acc,
                'n_samples': len(X_train),
                'n_features': X_train.shape[1]
            }
            
        except Exception as e:
            logger.error(f"Error training SVM: {str(e)}")
            raise
    
    def optimize_hyperparameters(self, X_train, y_train):
        """
        Perform grid search to find optimal hyperparameters
        
        Args:
            X_train: Training features
            y_train: Training labels
        
        Returns:
            Best parameters
        """
        try:
            logger.info("Starting hyperparameter optimization...")
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X_train)
            
            # Parameter grid
            param_grid = {
                'C': [0.1, 1, 10, 100],
                'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
                'kernel': ['rbf', 'linear']
            }
            
            # Grid search with cross-validation
            grid_search = GridSearchCV(
                svm.SVC(probability=True, class_weight='balanced'),
                param_grid,
                cv=5,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_scaled, y_train)
            
            # Update classifier with best parameters
            self.classifier = grid_search.best_estimator_
            self.is_trained = True
            
            logger.info(f"Best parameters: {grid_search.best_params_}")
            logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
            
            return grid_search.best_params_
            
        except Exception as e:
            logger.error(f"Error in hyperparameter optimization: {str(e)}")
            raise
    
    def predict(self, features, top_k=5):
        """
        Predict matches for given features
        
        Args:
            features: Feature vector(s) to match
            top_k: Number of top matches to return
        
        Returns:
            Predictions with confidence scores
        """
        try:
            if not self.is_trained:
                raise ValueError("Model must be trained before prediction")
            
            # Ensure 2D array
            if len(features.shape) == 1:
                features = features.reshape(1, -1)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Get probability predictions
            probabilities = self.classifier.predict_proba(features_scaled)
            classes = self.classifier.classes_
            
            # Get top-k predictions
            results = []
            for i, probs in enumerate(probabilities):
                # Sort by probability
                top_indices = np.argsort(probs)[::-1][:top_k]
                
                predictions = [
                    {
                        'class': classes[idx],
                        'confidence': float(probs[idx]),
                        'rank': rank + 1
                    }
                    for rank, idx in enumerate(top_indices)
                ]
                
                results.append(predictions)
            
            return results if len(results) > 1 else results[0]
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise
    
    def find_similar(self, query_features, database_features, database_ids, top_k=10, threshold=0.5):
        """
        Find similar records using cosine similarity
        
        Args:
            query_features: Query feature vector
            database_features: Database of feature vectors
            database_ids: Corresponding record IDs
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of matches with similarity scores
        """
        try:
            # Calculate cosine similarity
            query_norm = query_features / (np.linalg.norm(query_features) + 1e-6)
            
            similarities = []
            for i, db_features in enumerate(database_features):
                db_norm = db_features / (np.linalg.norm(db_features) + 1e-6)
                similarity = np.dot(query_norm, db_norm)
                
                if similarity >= threshold:
                    similarities.append({
                        'record_id': database_ids[i],
                        'similarity': float(similarity),
                        'confidence': float(similarity)  # Use similarity as confidence
                    })
            
            # Sort by similarity
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Add rank
            for rank, match in enumerate(similarities[:top_k], 1):
                match['rank'] = rank
            
            logger.info(f"Found {len(similarities)} matches above threshold {threshold}")
            
            return similarities[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar records: {str(e)}")
            raise
    
    def save_model(self, path):
        """Save SVM model and scaler"""
        try:
            model_data = {
                'classifier': self.classifier,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, path)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise
    
    def load_model(self, path):
        """Load SVM model and scaler"""
        try:
            if os.path.exists(path):
                model_data = joblib.load(path)
                self.classifier = model_data['classifier']
                self.scaler = model_data['scaler']
                self.is_trained = model_data['is_trained']
                logger.info(f"Model loaded from {path}")
            else:
                logger.warning(f"Model file not found: {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def get_model_info(self):
        """Get model information"""
        return {
            'kernel': self.classifier.kernel,
            'C': self.classifier.C,
            'gamma': self.classifier.gamma,
            'n_support': self.classifier.n_support_.tolist() if hasattr(self.classifier, 'n_support_') else None,
            'is_trained': self.is_trained
        }
