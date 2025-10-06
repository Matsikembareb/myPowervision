import json
import sys
import os
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from myPowervision import app, db
from myPowervision.models import *

def backup_database():
    """Backup all data from the database"""
    with app.app_context():
        backup_data = {
            'users': [],
            'roles': [],
            'permissions': [],
            'departments': [],
            'positions': [],
            'staff': [],
            'customers': [],
            'jobs': [],
            'vehicles': [],
            'role_permissions': []
        }

        print("Starting database backup...")

        # Backup Users
        try:
            for user in User.query.all():
                backup_data['users'].append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'role_id': getattr(user, 'role_id', None),
                    'activity_status': getattr(user, 'activity_status', 'offline'),
                    'availability_status': getattr(user, 'availability_status', 'available'),
                    'approval_status': getattr(user, 'approval_status', 'pending'),
                    'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None,
                    'last_seen': user.last_seen.isoformat() if hasattr(user, 'last_seen') and user.last_seen else None,
                    'last_login': user.last_login.isoformat() if hasattr(user, 'last_login') and user.last_login else None
                })
            print(f"✓ Users backed up: {len(backup_data['users'])}")
        except Exception as e:
            print(f"⚠ Users backup error: {e}")

        # Backup Roles
        try:
            for role in Role.query.all():
                backup_data['roles'].append({
                    'id': role.id,
                    'name': role.name,
                    'description': role.description
                })
            print(f"✓ Roles backed up: {len(backup_data['roles'])}")
        except Exception as e:
            print(f"⚠ Roles backup error: {e}")

        # Backup Permissions
        try:
            for perm in Permission.query.all():
                backup_data['permissions'].append({
                    'id': perm.id,
                    'permission': perm.permission,
                    'description': perm.description
                })
            print(f"✓ Permissions backed up: {len(backup_data['permissions'])}")
        except Exception as e:
            print(f"⚠ Permissions backup error: {e}")

        # Backup Role-Permission relationships
        try:
            from sqlalchemy import text
            role_perms = db.session.execute(text('SELECT role_id, permission_id FROM role_permission')).fetchall()
            backup_data['role_permissions'] = [{'role_id': rp[0], 'permission_id': rp[1]} for rp in role_perms]
            print(f"✓ Role-Permission relationships backed up: {len(backup_data['role_permissions'])}")
        except Exception as e:
            print(f"⚠ Role-Permission backup error: {e}")

        # Backup Departments
        try:
            for dept in Department.query.all():
                backup_data['departments'].append({
                    'id': dept.id,
                    'name': dept.name,
                    'description': dept.description
                })
            print(f"✓ Departments backed up: {len(backup_data['departments'])}")
        except Exception as e:
            print(f"⚠ Departments backup error: {e}")

        # Backup Positions
        try:
            for pos in Position.query.all():
                backup_data['positions'].append({
                    'id': pos.id,
                    'title': pos.title,
                    'description': pos.description
                })
            print(f"✓ Positions backed up: {len(backup_data['positions'])}")
        except Exception as e:
            print(f"⚠ Positions backup error: {e}")

        # Backup Staff
        try:
            for staff in Staff.query.all():
                backup_data['staff'].append({
                    'id': staff.id,
                    'staff_number': staff.staff_number,
                    'name': staff.name,
                    'surname': staff.surname,
                    'email': staff.email,
                    'phone': staff.phone,
                    'user_id': staff.user_id,
                    'department_id': staff.department_id,
                    'position_id': staff.position_id,
                    'hire_date': staff.hire_date.isoformat() if hasattr(staff, 'hire_date') and staff.hire_date else None,
                    'salary': getattr(staff, 'salary', None),
                    'allowances_worth': getattr(staff, 'allowances_worth', None),
                    'deductions_worth': getattr(staff, 'deductions_worth', None),
                    'bank_name': getattr(staff, 'bank_name', None),
                    'bank_account_number': getattr(staff, 'bank_account_number', None),
                    'bank_account_type': getattr(staff, 'bank_account_type', None)
                })
            print(f"✓ Staff backed up: {len(backup_data['staff'])}")
        except Exception as e:
            print(f"⚠ Staff backup error: {e}")

        # Backup Customers
        try:
            for customer in Customer.query.all():
                backup_data['customers'].append({
                    'id': customer.id,
                    'contact_person': customer.contact_person,
                    'customer_number': customer.customer_number,
                    'email': customer.email,
                    'company_name': customer.company_name,
                    'phone': customer.phone,
                    'address': customer.address,
                    'billing_address': customer.billing_address,
                    'notes': customer.notes,
                    'relationship_status': getattr(customer, 'relationship_status', 'good'),
                    'created_at': customer.created_at.isoformat() if hasattr(customer, 'created_at') and customer.created_at else None,
                    'updated_at': customer.updated_at.isoformat() if hasattr(customer, 'updated_at') and customer.updated_at else None
                })
            print(f"✓ Customers backed up: {len(backup_data['customers'])}")
        except Exception as e:
            print(f"⚠ Customers backup error: {e}")

        # Backup Jobs
        try:
            for job in Job.query.all():
                backup_data['jobs'].append({
                    'id': job.id,
                    'title': job.title,
                    'description': job.description,
                    'status': job.status,
                    'customer_id': job.customer_id,
                    'assigned_to_id': job.assigned_to_id,
                    'created_by_id': job.created_by_id,
                    'payment_terms': job.payment_terms,
                    'notes': job.notes,
                    'created_at': job.created_at.isoformat() if job.created_at else None,
                    'updated_at': job.updated_at.isoformat() if job.updated_at else None,
                    'date_scheduled': job.date_scheduled.isoformat() if job.date_scheduled else None,
                    'date_completed': job.date_completed.isoformat() if job.date_completed else None,
                    'time_allocated': getattr(job, 'time_allocated', None),
                    'contact_person': getattr(job, 'contact_person', None),
                    'job_number': getattr(job, 'job_number', None),
                    'invoice_number': getattr(job, 'invoice_number', None),
                    'vehicle_id': getattr(job, 'vehicle_id', None),
                    'stores_confirmation': getattr(job, 'stores_confirmation', False),
                    'work_done': getattr(job, 'work_done', False),
                    'technical_manager_approval': getattr(job, 'technical_manager_approval', False),
                    'accounts_payment': getattr(job, 'accounts_payment', False)
                })
            print(f"✓ Jobs backed up: {len(backup_data['jobs'])}")
        except Exception as e:
            print(f"⚠ Jobs backup error: {e}")

        # Backup Vehicles
        try:
            for vehicle in Vehicle.query.all():
                backup_data['vehicles'].append({
                    'id': vehicle.id,
                    'vehicle_number': vehicle.vehicle_number,
                    'make': vehicle.make,
                    'model': vehicle.model,
                    'year': getattr(vehicle, 'year', None),
                    'color': getattr(vehicle, 'color', None),
                    'vehicle_type': getattr(vehicle, 'vehicle_type', None),
                    'fuel_type': getattr(vehicle, 'fuel_type', None),
                    'capacity': getattr(vehicle, 'capacity', None),
                    'status': getattr(vehicle, 'status', 'available'),
                    'mileage': getattr(vehicle, 'mileage', None),
                    'notes': getattr(vehicle, 'notes', None),
                    'created_at': vehicle.created_at.isoformat() if hasattr(vehicle, 'created_at') and vehicle.created_at else None,
                    'updated_at': vehicle.updated_at.isoformat() if hasattr(vehicle, 'updated_at') and vehicle.updated_at else None,
                    'last_service_date': vehicle.last_service_date.isoformat() if hasattr(vehicle, 'last_service_date') and vehicle.last_service_date else None,
                    'next_service_date': vehicle.next_service_date.isoformat() if hasattr(vehicle, 'next_service_date') and vehicle.next_service_date else None,
                    'insurance_expiry': vehicle.insurance_expiry.isoformat() if hasattr(vehicle, 'insurance_expiry') and vehicle.insurance_expiry else None
                })
            print(f"✓ Vehicles backed up: {len(backup_data['vehicles'])}")
        except Exception as e:
            print(f"⚠ Vehicles backup error: {e}")

        # Save backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'database_backup_{timestamp}.json'

        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)

        print(f"\n✅ Complete backup saved to: {filename}")
        return filename

if __name__ == "__main__":
    backup_database()