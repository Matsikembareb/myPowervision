import json
import sys
import os
import glob
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from myPowervision import app, db
from myPowervision.models import *
import sqlalchemy as sa

def restore_database():
    """Restore all data to the database"""
    with app.app_context():
        # Find the latest backup file
        backup_files = glob.glob('database_backup_*.json')
        if not backup_files:
            print('❌ No backup file found!')
            return

        filename = max(backup_files)  # Use the latest backup
        print(f'📁 Using backup file: {filename}')

        with open(filename, 'r') as f:
            backup_data = json.load(f)

        # Restore in order (respecting foreign key dependencies)

        # 1. Restore Roles first
        print('\n🔄 Restoring Roles...')
        for role_data in backup_data['roles']:
            role = Role(
                name=role_data['name'],
                description=role_data['description']
            )
            db.session.add(role)
        db.session.commit()
        print(f'✓ Roles restored: {len(backup_data["roles"])}')

        # 2. Restore Permissions
        print('\n🔄 Restoring Permissions...')
        for perm_data in backup_data['permissions']:
            permission = Permission(
                permission=perm_data['permission'],
                description=perm_data['description']
            )
            db.session.add(permission)
        db.session.commit()
        print(f'✓ Permissions restored: {len(backup_data["permissions"])}')

        # 3. Restore Role-Permission relationships
        print('\n🔄 Restoring Role-Permission relationships...')
        for rp_data in backup_data['role_permissions']:
            try:
                db.session.execute(
                    sa.insert(role_permission).values(
                        role_id=rp_data['role_id'],
                        permission_id=rp_data['permission_id']
                    )
                )
            except Exception as e:
                print(f'⚠ Role-Permission relationship error: {e}')
        db.session.commit()
        print(f'✓ Role-Permission relationships restored: {len(backup_data["role_permissions"])}')

        # 4. Restore Users
        print('\n🔄 Restoring Users...')
        for user_data in backup_data['users']:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                role_id=user_data.get('role_id'),
                activity_status=user_data.get('activity_status', 'offline'),
                availability_status=user_data.get('availability_status', 'available'),
                approval_status=user_data.get('approval_status', 'pending')
            )
            
            if user_data.get('created_at'):
                user.created_at = datetime.fromisoformat(user_data['created_at'])
            if user_data.get('last_seen'):
                user.last_seen = datetime.fromisoformat(user_data['last_seen'])
            if user_data.get('last_login'):
                user.last_login = datetime.fromisoformat(user_data['last_login'])
            
            db.session.add(user)
        db.session.commit()
        print(f'✓ Users restored: {len(backup_data["users"])}')

        # 5. Restore Departments
        print('\n🔄 Restoring Departments...')
        for dept_data in backup_data['departments']:
            department = Department(
                name=dept_data['name'],
                description=dept_data['description']
            )
            db.session.add(department)
        db.session.commit()
        print(f'✓ Departments restored: {len(backup_data["departments"])}')

        # 6. Restore Positions
        print('\n🔄 Restoring Positions...')
        for pos_data in backup_data['positions']:
            position = Position(
                title=pos_data['title'],
                description=pos_data['description']
            )
            db.session.add(position)
        db.session.commit()
        print(f'✓ Positions restored: {len(backup_data["positions"])}')

        # 7. Restore Staff
        print('\n🔄 Restoring Staff...')
        for staff_data in backup_data['staff']:
            staff = Staff(
                staff_number=staff_data['staff_number'],
                name=staff_data['name'],
                surname=staff_data['surname'],
                email=staff_data['email'],
                phone=staff_data['phone'],
                user_id=staff_data['user_id'],
                department_id=staff_data['department_id'],
                position_id=staff_data['position_id'],
                salary=staff_data.get('salary'),
                allowances_worth=staff_data.get('allowances_worth'),
                deductions_worth=staff_data.get('deductions_worth'),
                bank_name=staff_data.get('bank_name'),
                bank_account_number=staff_data.get('bank_account_number'),
                bank_account_type=staff_data.get('bank_account_type')
            )
            
            if staff_data.get('hire_date'):
                staff.hire_date = datetime.fromisoformat(staff_data['hire_date']).date()
            
            db.session.add(staff)
        db.session.commit()
        print(f'✓ Staff restored: {len(backup_data["staff"])}')

        # 8. Restore Customers
        print('\n🔄 Restoring Customers...')
        for customer_data in backup_data['customers']:
            customer = Customer(
                contact_person=customer_data['contact_person'],
                customer_number=customer_data['customer_number'],
                email=customer_data['email'],
                company_name=customer_data['company_name'],
                phone=customer_data['phone'],
                address=customer_data.get('address'),
                billing_address=customer_data.get('billing_address'),
                notes=customer_data.get('notes'),
                relationship_status=customer_data.get('relationship_status', 'good')
            )
            
            if customer_data.get('created_at'):
                customer.created_at = datetime.fromisoformat(customer_data['created_at'])
            if customer_data.get('updated_at'):
                customer.updated_at = datetime.fromisoformat(customer_data['updated_at'])
            
            db.session.add(customer)
        db.session.commit()
        print(f'✓ Customers restored: {len(backup_data["customers"])}')

        # 9. Restore Vehicles
        print('\n🔄 Restoring Vehicles...')
        for vehicle_data in backup_data['vehicles']:
            vehicle = Vehicle(
                vehicle_number=vehicle_data['vehicle_number'],
                make=vehicle_data.get('make'),
                model=vehicle_data.get('model'),
                year=vehicle_data.get('year'),
                color=vehicle_data.get('color'),
                vehicle_type=vehicle_data.get('vehicle_type'),
                fuel_type=vehicle_data.get('fuel_type'),
                capacity=vehicle_data.get('capacity'),
                status=vehicle_data.get('status', 'available'),
                mileage=vehicle_data.get('mileage'),
                notes=vehicle_data.get('notes')
            )
            
            if vehicle_data.get('created_at'):
                vehicle.created_at = datetime.fromisoformat(vehicle_data['created_at'])
            if vehicle_data.get('updated_at'):
                vehicle.updated_at = datetime.fromisoformat(vehicle_data['updated_at'])
            if vehicle_data.get('last_service_date'):
                vehicle.last_service_date = datetime.fromisoformat(vehicle_data['last_service_date'])
            if vehicle_data.get('next_service_date'):
                vehicle.next_service_date = datetime.fromisoformat(vehicle_data['next_service_date'])
            if vehicle_data.get('insurance_expiry'):
                vehicle.insurance_expiry = datetime.fromisoformat(vehicle_data['insurance_expiry'])
            
            db.session.add(vehicle)
        db.session.commit()
        print(f'✓ Vehicles restored: {len(backup_data["vehicles"])}')

        # 10. Restore Jobs (last due to multiple foreign keys)
        print('\n🔄 Restoring Jobs...')
        for job_data in backup_data['jobs']:
            job = Job(
                title=job_data['title'],
                description=job_data.get('description'),
                status=job_data.get('status', 'pending'),
                customer_id=job_data.get('customer_id'),
                assigned_to_id=job_data.get('assigned_to_id'),
                created_by_id=job_data.get('created_by_id'),
                payment_terms=job_data.get('payment_terms'),
                notes=job_data.get('notes'),
                time_allocated=job_data.get('time_allocated'),
                contact_person=job_data.get('contact_person'),
                job_number=job_data.get('job_number'),
                invoice_number=job_data.get('invoice_number'),
                vehicle_id=job_data.get('vehicle_id'),
                stores_confirmation=job_data.get('stores_confirmation', False),
                work_done=job_data.get('work_done', False),
                technical_manager_approval=job_data.get('technical_manager_approval', False),
                accounts_payment=job_data.get('accounts_payment', False)
            )
            
            if job_data.get('created_at'):
                job.created_at = datetime.fromisoformat(job_data['created_at'])
            if job_data.get('updated_at'):
                job.updated_at = datetime.fromisoformat(job_data['updated_at'])
            if job_data.get('date_scheduled'):
                job.date_scheduled = datetime.fromisoformat(job_data['date_scheduled'])
            if job_data.get('date_completed'):
                job.date_completed = datetime.fromisoformat(job_data['date_completed'])
            
            db.session.add(job)
        db.session.commit()
        print(f'✓ Jobs restored: {len(backup_data["jobs"])}')

        print('\n🎉 All data restored successfully!')
        print('\n📊 Final counts:')
        print(f'Users: {User.query.count()}')
        print(f'Jobs: {Job.query.count()}')
        print(f'Customers: {Customer.query.count()}')
        print(f'Vehicles: {Vehicle.query.count()}')
        print(f'Staff: {Staff.query.count()}')
        print(f'Departments: {Department.query.count()}')
        print(f'Positions: {Position.query.count()}')
        print(f'Roles: {Role.query.count()}')
        print(f'Permissions: {Permission.query.count()}')

if __name__ == "__main__":
    restore_database()