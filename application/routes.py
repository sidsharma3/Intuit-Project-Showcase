from flask import flash, send_file, redirect, Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import InventoryItem, Inventory, User
import csv
from . import db

routes = Blueprint('routes', __name__)

# define routes
@routes.route('/', methods=['GET'])
def inventoryList():
    # Shows all the inventory items as a list
    return render_template("inventoryList.html", inventory=Inventory.query.get(1), curUser=current_user)

@routes.route('/delete', methods=['POST'])
@login_required
def delete():
    # This line of code will find the InventoryItem to Delete
    itemIdToDelete = request.form.get('deleteId')
    itemToDelete = InventoryItem.query.get(itemIdToDelete)
    # If the InventoryItem is found we delete it
    if itemToDelete != None:
        db.session.delete(itemToDelete)
        db.session.commit()
        flash('Inventory Item Deleted!')
    # Otherwise we let the user know the Inventory Item was not found
    else:
        flash('Inventory Item Not Found', category='issue')
    return redirect("/")

@routes.route("/getProductData")
@login_required
def downloadProductDataCSV():
    if (current_user.username != "admin"):
        flash('Must be an Administrator to Download Product Data', category='issue')
        return redirect("/")
    else:
        # Header Row for the CSV File
        headerRow = ['Product Name', 'Product Description', 'Quantity']
        # Build the CSV file
        with open ('ProductData.csv','w', newline='') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(headerRow)
            curInventory = Inventory.query.get(1)
            # This will get the current Inventory and if it is not empty
            # The for loop will add all the InventoryItem data in the InvetoryList
            # to the CSV file
            if curInventory != None:
                inventoryList = curInventory.allInventoryItems
                for inventoryItem in inventoryList:
                    curRow = []
                    curRow.append(inventoryItem.name)
                    curRow.append(inventoryItem.description)
                    curRow.append(inventoryItem.quantity)
                    filewriter.writerow(curRow)
        # These options return the CSV file for download without opening a new tab
        return send_file('../ProductData.csv',
                        mimetype='text/csv',
                        attachment_filename='ProductData.csv',
                        as_attachment=True)

@routes.route('/<editId>', methods=['GET', 'POST'])
@login_required
def edit(editId):
    # This query will get the correct InventoryItem to edit
    itemToEdit = InventoryItem.query.get(editId)
    # if the item is None that means the inventory item was not found thus we flash
    # an error message and return to the home screen.
    if itemToEdit == None:
        flash('Inventory Item Not Found', category='issue')
        return redirect("/")
    # if this is a GET request we pass the InventoryItem to edit
    # to the template so it can be used as the default values in the form
    # therefore the user does not need to retype any information they do not
    # wish to change
    if request.method == 'GET':
        return render_template("inventoryForm.html", item=itemToEdit, curUser=current_user)
    # if this is a POST request we make sure that itemToEdit is not None
    # then we get the new values from the form
    newName = request.form.get('name')
    newQuantity = request.form.get('quantity')
    newDescription = request.form.get('description')
    # Now we will get the form data and run the checks if there is an error
    # we will flash a message indicating the error to the user
    if len(newName) == 0:
        flash('Inventory Item Name Must Be At Least One Character Long', category='issue')
    elif len(newDescription) < 5:
        flash('Inventory Item Description Must Be At Least Five Characters Long', category='issue')
    elif len(newName) > 100:
        flash('Inventory Item Name Must Be At Most 100 Characters Long', category='issue')
    elif len(newDescription) > 500:
        flash('Inventory Item Description Must Be At Most 500 Characters Long', category='issue')
    elif newQuantity.isdigit() == False:
        flash('Inventory Item Quantity Must Be An Integer', category='issue')
    elif int(newQuantity) <= 0:
        flash('Inventory Item Quantity Must Be Greater Than 0', category='issue')
    else:
        # Reaching this case means all the data given is correct
        # thus now we can update the Inventory Item
        itemToEdit.name = newName
        itemToEdit.quantity = newQuantity
        itemToEdit.description = newDescription
        db.session.commit()
        flash('Inventory Item Updated!', category='success')
        return redirect("/")

    # if there is an error we stay on the screen with the form
    return render_template("inventoryForm.html", item=itemToEdit, curUser=current_user)


@routes.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # This code will initialize the Inventory List which will hold the Inventory Items
        # if no such list was made before.
        if not(db.session.query(db.exists().where(Inventory.id == 1)).scalar()):
            inventoryList = Inventory()
            db.session.add(inventoryList)
            db.session.commit()

        # Now we will get the form data and run the checks if there is an error
        # we will flash a message indicating the error to the user
        newName = request.form.get('name')
        newQuantity = request.form.get('quantity')
        newDescription = request.form.get('description')
        if len(newName) == 0:
            flash('Inventory Item Name Must Be At Least One Character Long', category='issue')
        elif len(newDescription) < 5:
            flash('Inventory Item Description Must Be At Least Five Characters Long', category='issue')
        elif len(newName) > 100:
            flash('Inventory Item Name Must Be At Most 100 Characters Long', category='issue')
        elif len(newDescription) > 500:
            flash('Inventory Item Description Must Be At Most 500 Characters Long', category='issue')
        elif newQuantity.isdigit() == False:
            flash('Inventory Item Quantity Must Be An Integer', category='issue')
        elif int(newQuantity) <= 0:
            flash('Inventory Item Quantity Must Be Greater Than 0', category='issue')
        else:
            # Reaching this case means all the data given is correct
            # therefore we can make the new Inventory Item
            newInventoryItem = InventoryItem(name=newName, quantity=newQuantity, description=newDescription, inventoryId=1, userId=current_user.id)
            db.session.add(newInventoryItem)
            db.session.commit()
            # Send the Success Message to the User
            flash('New Inventory Item Added!', category='success')
            # After adding the new Inventory Item we can redirect the user
            # to the home page to see the list of the inventory items
            return redirect("/")

    # if there is an error or the request was a GET request
    # then we should return the view showing the create Inventory Item Form
    return render_template("inventoryForm.html", item=None, curUser=current_user)
