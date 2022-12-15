# Help users navigate the app by adding tooltips
The application features a Tooltip function. Tooltips are small messages helping the user. These messages can be used to inform the user about the specifics of different functions and to guide the user to create surveys correctly. Tooltips appear on the page as small information icons. When the user hovers above the icon, the message is displayed. See the image below.


<img src="Images/TooltipTutorial1.png" width=260 />  

## Creating a tooltip
Tooltips can be created with the [tooltip macro](https://github.com/QueryAdmin-ohtu/SuperAdmin3000/blob/dev_juan/src/templates/components/macros/tooltip.html). The macro takes in one parameter called `text` which is the message to display to the user. To use the macro you have to import the file in the Jinja template. See example below.

```
{% import "components/macros/tooltip.html" as tooltip %}
{% import "components/macros/form_elements.html" as form_elements %}

<div class="flex flex-col gap-2 w-full">
  <div class="flex flex-row gap-2 w-full">
    {{ form_elements.label("survey", "Description")}}
    {{ tooltip.tooltip("A flavor text for the survey") }}
  </div>
  {{ form_elements.text_area("survey", "Description", "A short description", true) }}
</div>
```
