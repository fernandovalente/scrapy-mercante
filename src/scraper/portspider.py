from utils import (
    driver_setup,
    reach_main_page,
    go_to_search_main_page,
    select_consult_option,
    do_portcall_search,
    end_driver,
)

portcall_sample_value = "20000350812"


# Copy geckodriver to /var/bin

driver = driver_setup()

reach_main_page(driver)

go_to_search_main_page(driver)

select_consult_option(driver)

driver.switch_to.default_content()

do_portcall_search(driver, portcall_sample_value)

end_driver(driver)