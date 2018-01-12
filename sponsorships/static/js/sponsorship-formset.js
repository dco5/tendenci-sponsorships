function Formset(formsetsWrapper, prefix) {
    /*
        Dynamic Formset handler for Django formsets.

        Events:

            * init.formset
            * add-form.formset
            * remove-form.formset
            * renumber-form.formset

    */

    if (!(this instanceof Formset)) {
        return new Formset(formsetsWrapper)
    }

    prefix = typeof prefix === 'undefined' ? 'form' : prefix;

    var formset = this;
    var emptyForm = formsetsWrapper.querySelector('.empty-form').firstElementChild;
    var formsList = formsetsWrapper.querySelector('.extra-forms');

    var initialForms = formsetsWrapper.querySelector('[name$=' + prefix + '-INITIAL_FORMS]');
    var totalForms = formsetsWrapper.querySelector('[name$=' + prefix + '-TOTAL_FORMS]');
    prefix = initialForms.name.replace(/INITIAL_FORMS/, '');

    function renumberForm(form, oldValue, newValue) {
        // the convention for formsets is "prefix-numberOfFormset"
        var matchValue = prefix + oldValue.toString();
        var match = new RegExp(matchValue);
        var replace = prefix + newValue.toString();

        ['name', 'id', 'for'].forEach(function (attr) {
            form.querySelectorAll('[' + attr + '*=' + matchValue + ']').forEach(function (elem) {
                elem.setAttribute(attr, elem.getAttribute(attr).replace(match, replace))
            })
        });

        formsetsWrapper.dispatchEvent(new CustomEvent('renumber-form.formset',
            {
                detail: {
                    form: form,
                    oldValue: oldValue,
                    newValue: newValue,
                    formset: formset
                }
            })
        );
    }

    function getForm(target) {
        var parent = target.parentElement;
        // went too far
        if (parent === document) {
            return null;
        }
        // If the parent is the formList, then the element is a formset and that is what needs to be returned.
        if (parent === formsList) {
            return target;
        }
        // keep going up the ladder until the parent of the element is formList
        return getForm(parent);
    }

    function removeForm(event) {
        // Find the form "row": the child of the formsList that the parent of the element that triggered the event.
        var formToRemove = getForm(event.target);
        //Renumber the rows that come after the formset that is going to be removed.
        var nextElement = formToRemove.nextElementSibling;
        var nextElementIndex = Array.prototype.indexOf.call(formsList.children, formToRemove);
        while (nextElement) {
            renumberForm(nextElement, nextElementIndex + 1, nextElementIndex);
            {
                nextElement = nextElement.nextElementSibling;
                nextElementIndex = nextElementIndex + 1;
            }
        }
        //Remove this formset.
        formToRemove.remove();
        formsetsWrapper.dispatchEvent(new CustomEvent('remove-form.formset', {
            detail: {
                form: formToRemove,
                formset: formset
            }
        }));

        // Decrement the management from's count.
        totalForms.value = Number(totalForms.value) - 1;
    }

    function addForm(event) {
        // Duplicate empty form.
        var newForm = emptyForm.cloneNode(true);
        // Update all references to __prefix__ in the elements names with the current number of total forms.
        renumberForm(newForm, '__prefix__', totalForms.value);

        newForm.querySelector('[data-formset-remove-form]').addEventListener('click', removeForm);

        // Append the new form to the formsList.
        formsList.insertAdjacentElement('beforeend', newForm);
        formsetsWrapper.dispatchEvent(new CustomEvent('add-form.formset', {
            detail: {
                form: newForm,
                formset: formset
            }
        }));
        // Update the totalForms.value
        totalForms.value = Number(totalForms.value) + 1;
    }

    // Hookup the add formset button
    var addFormsetBtn = formsetsWrapper.querySelector('[data-formset-add-form]');

    addFormsetBtn.addEventListener('click', addForm);

    formsetsWrapper.formset = this;
    formsetsWrapper.dispatchEvent(new CustomEvent('init.formset', {
        detail: {
            formset: this
        }
    }));

    this.addForm = addForm;
}